import random
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from cinema_playout import config
from cinema_playout.database import models
from cinema_playout.library import LibraryService
from tests.utils import random_feature, random_playlist_item, random_string


@pytest.fixture
def remote_library_items(db_session):
    """Creates remote library with a single feature on each day for 100 days"""
    start = datetime.now() - timedelta(days=50)
    for _ in range(100):
        feature = random_feature(db_session)
        fp = feature.remote_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()
        start += timedelta(days=1)
        random_playlist_item(db_session, feature_id=feature.id, start=start)


@pytest.fixture
def remote_hold_items():
    hold_items = []
    for _ in range(3):
        fp = Path(config.REMOTE_HOLD_VIDEO_PATH) / f"{random_string()}.mp4"
        hold_items.append(fp)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()
        fp = Path(config.REMOTE_HOLD_MUSIC_PATH) / f"{random_string()}.mp3"
        hold_items.append(fp)
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.touch()
    return hold_items


def test_copy_playlist_item(db_session, remote_library_items):
    item = models.Playlist.get_next_item(db_session, start=datetime.now(), content_type=models.ContentType.Feature)
    assert item is not None
    feature = models.Feature.get_by_id(db_session, id=item.content_id)
    assert feature is not None
    assert feature.remote_path.exists()
    assert not feature.local_path.exists()
    library = LibraryService(db_session)
    library._copy_playlist_item(feature)
    assert feature.local_path.exists()


def test_copy_playlist_items(db_session, remote_library_items):
    start = datetime.now()
    end = start + timedelta(days=3)
    items = models.Playlist.get_between(db_session, start, end, content_type=models.ContentType.Feature)
    for item in items:
        feature = models.Feature.get_by_id(db_session, id=item.content_id)
        assert feature is not None
        assert feature.remote_path.exists()
        assert not feature.local_path.exists()
    # --- end setup
    library = LibraryService(db_session)
    library.copy_playlist_items(start, end, content_type=models.ContentType.Feature)
    for item in items:
        feature = models.Feature.get_by_id(db_session, id=item.content_id)
        assert feature.local_path.exists()


@pytest.mark.parametrize(
    "end_dur, threshold_dur",
    [
        (2, 1),
        (1, 1),
        (10, 5),
    ],
)
def test_remove_playlist_items(db_session, remote_library_items, end_dur, threshold_dur):
    start = datetime.now()
    end = start + timedelta(days=end_dur)
    library = LibraryService(db_session)
    library.copy_playlist_items(start, end, content_type=models.ContentType.Feature)
    # --- end setup
    threshold = start + timedelta(days=threshold_dur)
    library.remove_playlist_items(start, threshold, content_type=models.ContentType.Feature)
    items = models.Playlist.get_between(db_session, start, end, content_type=models.ContentType.Feature)
    for item in items:
        feature = models.Feature.get_by_id(db_session, id=item.content_id)
        assert feature is not None
        assert feature.remote_path.exists()
        if item.start <= threshold:
            assert feature.local_path.exists()
        else:
            assert not feature.local_path.exists()


def test_copy_hold_item():
    remote_hold_item = Path(config.REMOTE_HOLD_VIDEO_PATH) / f"{random_string()}.mp4"
    remote_hold_item.parent.mkdir(parents=True)
    remote_hold_item.touch()
    assert remote_hold_item.exists()
    local_hold_item = Path(config.LOCAL_LIBRARY_PATH) / remote_hold_item.relative_to(config.REMOTE_HOLD_ROOT_PATH)
    assert not local_hold_item.exists()
    library = LibraryService()
    library._copy_hold_item(remote_hold_item)
    assert local_hold_item.exists()


def test_copy_hold_items(remote_hold_items):
    library = LibraryService()
    library.copy_hold_items()
    for item in remote_hold_items:
        local_hold_item = Path(config.LOCAL_LIBRARY_PATH) / item.relative_to(config.REMOTE_HOLD_ROOT_PATH)
        assert local_hold_item.exists()


def test_remove_hold_items(db_session, remote_hold_items):
    library = LibraryService(db_session)
    library.copy_hold_items()
    for item in random.sample(remote_hold_items, 3):
        item.unlink()
    # --- end setup
    library.remove_hold_items()
    for item in remote_hold_items:
        local_hold_item = Path(config.LOCAL_LIBRARY_PATH) / item.relative_to(config.REMOTE_HOLD_ROOT_PATH)
        if item.exists():
            assert local_hold_item.exists
        else:
            assert not local_hold_item.exists()


# def test_remove_hold_items__warns_no_remote_content(log, remote_hold_items):
#     library = LibraryService()
#     library.copy_hold_items()
#     for item in remote_hold_items:
#         item.unlink()
#     # --- end setup
#     library.remove_hold_items()
#     assert log.has("No remote hold videos - will not delete local copies", level="warning")
#     assert log.has("No remote hold music - will not delete local copies", level="warning")
