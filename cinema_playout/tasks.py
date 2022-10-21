import asyncio
import shutil
from datetime import datetime, timedelta
from pathlib import Path

from cinema_playout import config
from cinema_playout.database.models.playlist_item import Feature, PlaylistItem
from cinema_playout.database.models.playlist import ContentType, Playlist
from cinema_playout.database.session import Session
from cinema_playout.loggerfactory import LoggerFactory

logger = LoggerFactory.get_logger("tasks")


def copy_playlist_item_to_playout(item: PlaylistItem):
    """
    Copy a remote playlist item to local storage.
    File paths are stored in database as full CIFS share path... which I can't change.
    """
    src = item.remote_path
    dest = item.local_path
    logger.debug(f"Checking {src} for copy")
    if not src.exists():
        logger.error(f"playlist item {src} does not exist in library")
        return
    if not config.DEBUG:
        if not dest.parent.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists():
            logger.info(f"Copying playlist item {src}")
            shutil.copyfile(src, dest)


async def copy_playlist_items():
    """Copy playlist items to playout."""
    start = datetime.now()
    end = start + timedelta(days=14)  # hardcoded value
    with Session() as db_session:
        playlist_items = Playlist.get_between(db_session, start, end)
        for pi in (pi for pi in playlist_items if pi.content_type == ContentType.Feature):
            feature = Feature.get_by_id(db_session, pi.content_id)
            copy_playlist_item_to_playout(feature)


async def remove_playlist_items():
    """
    Remove old playlist items from local storage.
    Keeps many distant playlist items in local storage for local playback if there were network issues.
    """
    start = datetime.now() - timedelta(days=14)  # hardcoded value
    end = start + timedelta(days=14)  # hardcoded value
    remote_files = []
    with Session() as db_session:
        playlist_items = Playlist.get_between(db_session, start, end)
        for pi in (pi for pi in playlist_items if pi.content_type == ContentType.Feature):
            feature = Feature.get_by_id(db_session, pi.content_id)
            remote_files.append(feature.remote_path.relative_to(config.REMOTE_LIBRARY_PATH))
    local_files = []
    for fp in (Path(config.LOCAL_LIBRARY_PATH) / "Movies").glob("**/*"):
        if fp.is_dir():
            continue
        local_files.append(fp.relative_to(config.LOCAL_LIBRARY_PATH))
    files_to_remove = set(local_files) - set(remote_files)
    for fp in files_to_remove:
        logger.info(f"Removing {fp}")
        if not config.DEBUG:
            (Path(config.LOCAL_LIBRARY_PATH) / fp).unlink()


async def copy_hold_item_to_playout(src: Path):
    """Copy a romote hold item to local storage."""
    logger.debug(f"Checking {src} for copy")
    if not src.exists():
        logger.error("hold item does not exist in library")
        return
    root_path = Path(config.REMOTE_LIBRARY_PATH) / f"CinemaPlayout/server-{config.SERVER_ID}"
    relative = src.relative_to(root_path)
    dest = Path(config.LOCAL_LIBRARY_PATH) / relative
    if not config.DEBUG:
        if not dest.parent.exists():
            dest.parent.mkdir()
        if not dest.exists():
            logger.info(f"Copying hold item {src}")
            await asyncio.to_thread(shutil.copyfile, src, dest)


async def copy_hold_items():
    """Copy hold items to playout."""
    videos = (Path(config.REMOTE_LIBRARY_PATH) / f"CinemaPlayout/server-{config.SERVER_ID}/hold-videos").glob("*")
    for i in videos:
        await copy_hold_item_to_playout(i)
    music = (Path(config.REMOTE_LIBRARY_PATH) / f"CinemaPlayout/server-{config.SERVER_ID}/hold-music").glob("*")
    for i in music:
        await copy_hold_item_to_playout(i)


async def remove_hold_items():
    remote_root_path = Path(config.REMOTE_LIBRARY_PATH) / f"CinemaPlayout/server-{config.SERVER_ID}"
    # remove videos
    local_files = [
        fp.relative_to(config.LOCAL_LIBRARY_PATH) for fp in (Path(config.LOCAL_LIBRARY_PATH) / "hold-videos").glob("*")
    ]
    remote_files = [
        fp.relative_to(remote_root_path)
        for fp in (Path(config.REMOTE_LIBRARY_PATH) / f"CinemaPlayout/server-{config.SERVER_ID}/hold-videos").glob("*")
    ]
    if len(remote_files) > 0:
        files_to_remove = set(local_files) - set(remote_files)
        for fp in files_to_remove:
            logger.info(f"Removing {fp}")
            if not config.DEBUG:
                (Path(config.LOCAL_LIBRARY_PATH) / fp).unlink()
    else:
        logger.warning("No remote hold videos - will not delete local copies")
    # remove music
    local_files = [
        fp.relative_to(config.LOCAL_LIBRARY_PATH) for fp in (Path(config.LOCAL_LIBRARY_PATH) / "hold-music").glob("*")
    ]
    remote_files = [
        fp.relative_to(remote_root_path)
        for fp in (Path(config.REMOTE_LIBRARY_PATH) / f"CinemaPlayout/server-{config.SERVER_ID}/hold-music").glob("*")
    ]
    if len(remote_files) > 0:
        files_to_remove = set(local_files) - set(remote_files)
        for fp in files_to_remove:
            logger.info(f"Removing {fp}")
            if not config.DEBUG:
                (Path(config.LOCAL_LIBRARY_PATH) / fp).unlink()
    else:
        logger.warning("No remote hold music - will not delete local copies")
