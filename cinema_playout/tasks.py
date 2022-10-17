import asyncio
import shutil
from datetime import datetime, timedelta
from pathlib import Path, PureWindowsPath

from cinema_playout.config import DEBUG, LOCAL_CINEMA_PATH, LOCAL_MEDIA_PATH, SERVER_ID
from cinema_playout.database.models.feature import Feature
from cinema_playout.database.models.playlist import Playlist
from cinema_playout.database.session import Session
from cinema_playout.loggerfactory import LoggerFactory

logger = LoggerFactory.get_logger("tasks")


async def copy_playlist_item_to_playout(src: PureWindowsPath):
    """
    Copy a remote playlist item to local storage.
    File paths are stored in database as full CIFS share path... which I can't change.
    """
    logger.info(f"Copying playlist item {src}")
    relative = src.relative_to("//10.0.0.126/media")  # hardcoded
    src = Path(LOCAL_CINEMA_PATH) / relative
    dest = Path(LOCAL_MEDIA_PATH) / relative
    if not DEBUG:
        if not dest.parent.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(shutil.copyfile, src, dest)


async def copy_playlist_items():
    """Copy playlist items to playout."""
    start = datetime.now()
    end = start + timedelta(days=14)  # hardcoded value
    with Session() as db_session:
        playlist_items = Playlist.get_between(db_session, start, end)
        for pi in (pi for pi in playlist_items if pi.content_type == "Feature"):
            feature = Feature.get_by_id(db_session, pi.content_id)
            fp = PureWindowsPath(feature._path)
            await copy_playlist_item_to_playout(fp)


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
        for pi in (pi for pi in playlist_items if pi.content_type == "Feature"):
            feature = Feature.get_by_id(db_session, pi.content_id)
            remote_files.append(PureWindowsPath(feature._path).relative_to("//10.0.0.126/media"))  # hardcoded)
    local_files = []
    for fp in (Path(LOCAL_MEDIA_PATH) / "Movies").glob("**/*"):
        if fp.is_dir():
            continue
        local_files.append(fp.relative_to(LOCAL_MEDIA_PATH))
    files_to_remove = set(local_files) - set(remote_files)
    for fp in files_to_remove:
        logger.info(f"Removing {fp}")
        if not DEBUG:
            (Path(LOCAL_MEDIA_PATH) / fp).unlink()


async def copy_hold_item_to_playout(src: Path):
    """Copy a romote hold item to local storage."""
    logger.info(f"Copying hold item {src}")
    root_path = Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}"
    relative = src.relative_to(root_path)
    dest = Path(LOCAL_MEDIA_PATH) / relative
    if not DEBUG:
        if not dest.parent.exists():
            dest.parent.mkdir()
        await asyncio.to_thread(shutil.copyfile, src, dest)


async def copy_hold_items():
    """Copy hold items to playout."""
    videos = (Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}/hold-videos").glob("*")
    for i in videos:
        await copy_hold_item_to_playout(i)
    music = (Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}/hold-music").glob("*")
    for i in music:
        await copy_hold_item_to_playout(i)


async def remove_hold_items():
    remote_root_path = Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}"
    # remove videos
    local_files = [fp.relative_to(LOCAL_MEDIA_PATH) for fp in (Path(LOCAL_MEDIA_PATH) / "hold-videos").glob("*")]
    remote_files = [
        fp.relative_to(remote_root_path)
        for fp in (Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}/hold-videos").glob("*")
    ]
    if len(remote_files) > 0:
        files_to_remove = set(local_files) - set(remote_files)
        for fp in files_to_remove:
            logger.info(f"Removing {fp}")
            if not DEBUG:
                (Path(LOCAL_MEDIA_PATH) / fp).unlink()
    else:
        logger.warning("No remote hold videos - will not delete local copies")
    # remove music
    local_files = [fp.relative_to(LOCAL_MEDIA_PATH) for fp in (Path(LOCAL_MEDIA_PATH) / "hold-music").glob("*")]
    remote_files = [
        fp.relative_to(remote_root_path)
        for fp in (Path(LOCAL_CINEMA_PATH) / f"CinemaPlayout/server-{SERVER_ID}/hold-music").glob("*")
    ]
    if len(remote_files) > 0:
        files_to_remove = set(local_files) - set(remote_files)
        for fp in files_to_remove:
            logger.info(f"Removing {fp}")
            if not DEBUG:
                (Path(LOCAL_MEDIA_PATH) / fp).unlink()
    else:
        logger.warning("No remote hold music - will not delete local copies")


# if __name__ == "__main__":
# asyncio.run(copy_playlist_items())
# asyncio.run(remove_playlist_items())
# asyncio.run(copy_hold_items())
# remove_hold_items()
