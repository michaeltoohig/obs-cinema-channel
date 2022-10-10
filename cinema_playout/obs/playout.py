import asyncio
import os
from datetime import datetime
from pathlib import Path

from cinema_playout.config import INFO_NEXT_PLAYING, INFO_NOW_PLAYING, LOCAL_CINEMA_PATH, SERVER_ID
from cinema_playout.database.models import Feature, Playlist
from cinema_playout.database.session import Session
from cinema_playout.loggerfactory import LoggerFactory
from cinema_playout.obs.client import OBSClient

logger = LoggerFactory.get_logger("obs.playout")


# TODO set path root to config - path accessible by Python
now_playing_file = Path(f"{LOCAL_CINEMA_PATH}/CinemaPlayout") / f"server-{SERVER_ID}" / INFO_NOW_PLAYING
next_playing_file = Path(f"{LOCAL_CINEMA_PATH}/CinemaPlayout") / f"server-{SERVER_ID}" / INFO_NEXT_PLAYING


async def setup_playout(client):
    """Setup playout OBS instance and configure callbacks."""
    # client.register_event_callback(on_mediaplaybackended, "MediaInputPlaybackEnded")
    pass


def set_now_playing(feature):
    now_playing_file.write_text(f"Now Playing: {str(feature)}")


def set_next_playing(feature, start):
    next_playing_file.write_text(f"Next @ {start.strftime('%I:%M %p')}: {str(feature)}")


async def show_feature_name_loop(client):
    """Secondary loop for displaying current feature name and next feature name on main feature scene."""
    await client.show_current_feature_name(False)
    await client.show_next_feature_name(False)
    while True:
        await asyncio.sleep(900)
        await client.show_current_feature_name(True)
        await asyncio.sleep(30)
        await client.show_current_feature_name(False)
        await asyncio.sleep(10)
        await client.show_next_feature_name(True)
        await asyncio.sleep(30)
        await client.show_next_feature_name(False)


async def playout_loop(client):
    """Main playout loop for cinema channel."""
    feature = None
    await client.request("OpenProjector", {"type": "Preview", "monitor": 1})

    while True:
        if not feature:
            with Session() as db_session:
                now = datetime.now()
                playlist_item = Playlist.get_item_at(db_session, now)

            if not playlist_item:
                logger.debug("No playlist item currently, checking again later")
                await client.play_hold()
                await asyncio.sleep(5)
                continue

            if playlist_item.content_type == "Feature":
                feature = Feature.get_by_id(db_session, playlist_item.content_id)
                logger.info(f"Got from playlist {feature}")
                set_now_playing(feature)
            else:
                logger.debug("Playlist item is not a feature, checking again later")
                await client.play_hold()
                await asyncio.sleep(5)
                continue
        else:
            offset = (datetime.now() - playlist_item.start).total_seconds() * 1000
            await client.play_feature(feature._path, offset)

            while datetime.now() < playlist_item.end:

                sleepUntil = (playlist_item.end - datetime.now()).total_seconds()
                if sleepUntil <= 15:
                    logger.debug(f"Final sleeping for {sleepUntil}")
                    await asyncio.sleep(sleepUntil)
                    break
                else:
                    with Session() as db_session:
                        next_playlist_item = Playlist.get_next_item(db_session, playlist_item.end)
                        next_feature = Feature.get_by_id(db_session, next_playlist_item.content_id)
                        set_next_playing(next_feature, next_playlist_item.start)
                    await asyncio.sleep(15)
            # reset feature to grab next one
            feature = None


def main_loop():
    loop = asyncio.get_event_loop()
    client = OBSClient(loop=loop)

    if not loop.run_until_complete(client.connect()):
        os._exit(1)

    # TODO add to a periodic update loop... but only during feature play
    loop.run_until_complete(client.update_hold_media())

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
