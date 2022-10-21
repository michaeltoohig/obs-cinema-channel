from datetime import datetime, timedelta
import pytest
from cinema_playout import config

from cinema_playout.database import models
from cinema_playout.tasks import copy_playlist_item_to_playout
from tests.utils import random_feature, random_playlist_item


@pytest.fixture
def populate_remote_library(db_session):
    start = datetime.now() - timedelta(days=50)
    for _ in range(100):
        feature = random_feature(db_session)
        fp = feature.local_path
        fp.parent.mkdir(parents=True, exist_ok=True)
        import pdb

        pdb.set_trace()
        fp.touch()
        start += timedelta(days=1)
        random_playlist_item(db_session, feature_id=feature.id, start=start)


# @pytest.mark.asyncio
def test_copy_playlist_item(db_session, populate_remote_library, tmp_path_factory):
    # local_library_path = tmp_path_factory.mktemp("local")
    # config.LOCAL_LIBRARY_PATH = str(local_library_path)
    # ---
    item = models.Playlist.get_next_item(db_session, start=datetime.now(), content_type=models.ContentType.Feature)
    assert item is not None
    feature = models.Feature.get_by_id(db_session, id=item.content_id)
    assert feature is not None
    assert feature.remote_path.exists()
    import pdb

    pdb.set_trace()
    assert not feature.local_path.exists()
    copy_playlist_item_to_playout(feature)
    assert feature.local_path.exists()
