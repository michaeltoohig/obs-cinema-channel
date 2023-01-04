from datetime import datetime, timedelta

import structlog

from cinema_playout import config
from cinema_playout.database.models.playlist import ContentType
from cinema_playout.database.session import Session
from cinema_playout.library import LibraryService

logger = structlog.get_logger()


def copy_playlist_items():
    """Copy playlist items to playout."""
    start = datetime.now()
    end = start + timedelta(days=config.LOCAL_LIBRARY_KEEP_FUTURE)
    with Session() as db_session:
        library = LibraryService(db_session)
        library.copy_playlist_items(start, end, content_type=ContentType.Feature)


def remove_playlist_items():
    """
    Remove old playlist items from local storage.
    Keeps many distant playlist items in local storage for local playback if there were network issues.
    """
    start = datetime.now() - timedelta(days=config.LOCAL_LIBRARY_KEEP_PAST)
    end = datetime.now() + timedelta(days=config.LOCAL_LIBRARY_KEEP_FUTURE)
    with Session() as db_session:
        library = LibraryService(db_session)
        library.remove_playlist_items(start, end, content_type=ContentType.Feature)


def copy_hold_items():
    """Copy hold items to playout."""
    library = LibraryService()
    library.copy_hold_items()


def remove_hold_items():
    library = LibraryService()
    library.remove_hold_items()
