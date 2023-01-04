from datetime import datetime, timedelta

from tests.utils import random_feature, random_playlist_item, random_string


def test_random_feature(db_session):
    name = random_string()
    year = 2022
    feature = random_feature(db_session, name=name, year=year)
    assert feature.id is not None
    assert feature.name == name
    assert feature.year == year


def test_random_playlist_item__feature(db_session):
    feature = random_feature(db_session)
    start = datetime.now()
    duration = 3600
    playlist_item = random_playlist_item(db_session, feature_id=feature.id, start=start, duration=duration)
    assert playlist_item.id is not None
    assert playlist_item.feature_id == feature.id
    assert playlist_item.start == start
    assert playlist_item.end == start + timedelta(seconds=duration)
