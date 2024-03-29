import asyncio
import os
from datetime import datetime
from pathlib import Path

import structlog
from apscheduler.schedulers.background import BackgroundScheduler

from cinema_playout import config
from cinema_playout.database.models import Feature, Playlist
from cinema_playout.database.models.playlist import ContentType
from cinema_playout.database.session import Session
from cinema_playout.obs.client import OBSClient
from cinema_playout.tasks import copy_hold_items, copy_playlist_items, remove_hold_items, remove_playlist_items

logger = structlog.get_logger()


now_playing_file = Path(config.REMOTE_HOLD_ROOT_PATH) / config.INFO_NOW_PLAYING
next_playing_file = Path(config.REMOTE_HOLD_ROOT_PATH) / config.INFO_NEXT_PLAYING


async def setup_playout(client):
    """Setup playout OBS instance and configure callbacks."""
    # client.register_event_callback(on_mediaplaybackended, "MediaInputPlaybackEnded")
    await client.show_current_feature_name(False)
    await client.show_next_feature_name(False)


def copy_content_to_local_storage():
    copy_playlist_items()
    remove_playlist_items()
    copy_hold_items()
    remove_hold_items()


def set_now_playing(feature):
    now_playing_file.write_text(f"Now Playing: {str(feature)}")


def set_next_playing(feature, start):
    next_playing_file.write_text(f"Next @ {start.strftime('%I:%M %p')}: {str(feature)}")


def update_next_playing():
    with Session() as db_session:
        next_playlist_feature = Playlist.get_next_item(db_session, datetime.now(), content_type=ContentType.Feature)
        next_feature = Feature.get_by_id(db_session, next_playlist_feature.content_id)
        logger.debug(f"Update next playing {next_feature}")
        set_next_playing(next_feature, next_playlist_feature.start)


def start_scheduler():
    """Scheduler to collect local media files."""
    scheduler = BackgroundScheduler()
    # Only copy during midnight hours due to playout performance issues
    scheduler.add_job(copy_content_to_local_storage, "cron", hour=3)
    scheduler.start()


async def show_feature_name_loop(client):
    """Secondary loop for displaying current feature name and next feature name on main feature scene."""
    await client.show_current_feature_name(False)
    await client.show_next_feature_name(False)
    while True:
        await asyncio.sleep(10)
        await client.show_current_feature_name(True)
        await asyncio.sleep(30)
        await client.show_current_feature_name(False)
        await asyncio.sleep(10)
        await client.show_next_feature_name(True)
        await asyncio.sleep(30)
        await client.show_next_feature_name(False)
        await asyncio.sleep(890)


async def playout_loop(client):
    """Main playout loop for cinema channel."""
    feature = None
    await client.open_fullscreen()

    while True:
        if not feature:
            # TODO get feature within next 30 seconds then start a countdown to begin
            now = datetime.now()
            with Session() as db_session:
                playlist_item = Playlist.get_item_at(db_session, now)

            if not playlist_item:
                logger.debug("No playlist item currently, checking again later")
                await client.play_hold()
                await asyncio.sleep(30)
                continue

            if playlist_item.content_type == ContentType.Feature:
                with Session() as db_session:
                    feature = Feature.get_by_id(db_session, playlist_item.content_id)
                if not feature.local_path.exists():
                    logger.error(f"Feature is not available in local storage. {feature}")
                    feature = None
                    await client.play_hold()
                    sleepUntil = (playlist_item.end - datetime.now()).total_seconds()
                    await asyncio.sleep(sleepUntil)
                    continue
                logger.info(f"Got from playlist {feature}")
                set_now_playing(feature)
            else:
                logger.debug("Playlist item is not a feature, checking again later")
                await client.play_hold()
                await asyncio.sleep(30)
                continue
        else:
            offset = (datetime.now() - playlist_item.start).total_seconds() * 1000
            await client.play_feature(feature.local_path, offset)
            await client.update_hold_media()
            update_next_playing()

            while datetime.now() < playlist_item.end:

                sleepUntil = (playlist_item.end - datetime.now()).total_seconds()
                if sleepUntil <= 60:
                    logger.debug(f"Final sleeping for {sleepUntil}")
                    await asyncio.sleep(max(1, sleepUntil - 1))
                    # Maybe add an event listener for end of video playback as cue to break
                    break
                else:
                    # update_next_playing()
                    await asyncio.sleep(60)
            # reset feature to grab next one
            feature = None


def main_loop():
    logger.info(f"Starting cinema {config.SERVER_ID}")
    loop = asyncio.get_event_loop()
    client = OBSClient(loop=loop)

    if not loop.run_until_complete(client.connect()):
        os._exit(1)

    loop.run_until_complete(client.update_hold_media())

    start_scheduler()
    update_next_playing()
    loop.create_task(playout_loop(client))
    loop.create_task(show_feature_name_loop(client))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        logger.exception("Exception:\n")
    finally:
        loop.run_until_complete(client.disconnect())
