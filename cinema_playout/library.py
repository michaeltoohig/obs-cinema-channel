from datetime import datetime
from pathlib import Path
import shutil

from cinema_playout import config
from cinema_playout.database.models.playlist import ContentType, Playlist
from cinema_playout.database.models.playlist_item import Feature, PlaylistItem

import structlog

logger = structlog.get_logger()


class LibraryService:
    """Service for managing library content on playout."""

    def __init__(self, session=None):
        self.session = session

    def _copyfile(self, src: Path, dest: Path):
        if not config.DEBUG:
            if not dest.parent.exists():
                dest.parent.mkdir(parents=True)
            if not dest.exists():
                logger.info(f"{src} is copying to local {dest}")
                shutil.copyfile(src, dest)

    def _copy_playlist_item(self, item: PlaylistItem):
        src = item.remote_path
        dest = item.local_path
        if not src.exists():
            logger.error(f"Playlist item {src} does not exist in library")
            return
        self._copyfile(src, dest)

    def copy_playlist_items(self, start: datetime, end: datetime, *, content_type: ContentType = None):
        assert self.session, "LibraryService must be initialized with SQLAlchemy session to use this method"
        items = Playlist.get_between(self.session, start, end, content_type=content_type)
        for i in items:
            feature = Feature.get_by_id(self.session, i.content_id)
            self._copy_playlist_item(feature)

    def remove_playlist_items(self, start: datetime, end: datetime, *, content_type: ContentType = None):
        assert self.session, "LibraryService must be initialized with SQLAlchemy session to use this method"
        # gather list of files to keep on playout
        keep_files = []
        items = Playlist.get_between(self.session, start, end, content_type=content_type)
        for i in items:
            feature = Feature.get_by_id(self.session, i.content_id)
            fp = feature.remote_path.relative_to(config.REMOTE_LIBRARY_PATH)
            keep_files.append(fp)
            logger.debug(f"{fp} to keep local")
        # gather list of files in local playout storage
        current_files = []
        for fp in (Path(config.LOCAL_LIBRARY_PATH) / "Movies").glob("**/*"):
            if fp.is_dir():
                continue
            fp = fp.relative_to(config.LOCAL_LIBRARY_PATH)
            current_files.append(fp)
            logger.debug(f"{fp} found in local")
        # remove files from local playout storage
        to_remove = set(current_files) - set(keep_files)
        for fp in to_remove:
            if not config.DEBUG:
                (Path(config.LOCAL_LIBRARY_PATH) / fp).unlink()
            logger.info(f"{fp} removed from local")

    def _copy_hold_item(self, src: Path):
        if not src.exists():
            logger.error(f"Hold item {src} does not exist in library")
            return
        dest = Path(config.LOCAL_LIBRARY_PATH) / src.relative_to(config.REMOTE_HOLD_ROOT_PATH)
        self._copyfile(src, dest)

    def copy_hold_items(self):
        videos = Path(config.REMOTE_HOLD_VIDEO_PATH).glob("*")
        for fp in videos:
            self._copy_hold_item(fp)
        music = Path(config.REMOTE_HOLD_MUSIC_PATH).glob("*")
        for fp in music:
            self._copy_hold_item(fp)

    def remove_hold_items(self):
        # remove hold videos from local storage
        keep_files = []
        for fp in Path(config.REMOTE_HOLD_VIDEO_PATH).glob("*"):
            fp = fp.relative_to(Path(config.REMOTE_HOLD_ROOT_PATH))
            keep_files.append(fp)
            logger.debug(f"{fp} to keep local")
        current_files = []
        for fp in (Path(config.LOCAL_LIBRARY_PATH) / "hold-videos").glob("*"):
            fp = fp.relative_to(config.LOCAL_LIBRARY_PATH)
            current_files.append(fp)
            logger.debug(f"{fp} found in local")
        if len(keep_files) > 0:
            to_remove = set(current_files) - set(keep_files)
            for fp in to_remove:
                if not config.DEBUG:
                    (Path(config.LOCAL_LIBRARY_PATH) / fp).unlink()
                logger.info(f"{fp} removed from local")
        else:
            logger.warn("No remote hold videos - will not delete local copies")
        # remove hold music from local storage
        keep_files = []
        for fp in Path(config.REMOTE_HOLD_MUSIC_PATH).glob("*"):
            fp = fp.relative_to(Path(config.REMOTE_HOLD_ROOT_PATH))
            keep_files.append(fp)
            logger.debug(f"{fp} to keep local")
        current_files = []
        for fp in (Path(config.LOCAL_LIBRARY_PATH) / "hold-music").glob("*"):
            fp = fp.relative_to(config.LOCAL_LIBRARY_PATH)
            current_files.append(fp)
            logger.debug(f"{fp} found in local")
        if len(keep_files) > 0:
            to_remove = set(current_files) - set(keep_files)
            for fp in to_remove:
                if not config.DEBUG:
                    (Path(config.LOCAL_LIBRARY_PATH) / fp).unlink()
                logger.info(f"{fp} removed from local")
        else:
            logger.warn("No remote hold music - will not delete local copies")
