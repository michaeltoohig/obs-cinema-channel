from datetime import datetime, timedelta
import random
import string

from cinema_playout import config
from cinema_playout.database import models


def random_string():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(10))


def random_feature(db_session, **kwargs):
    name = kwargs["name"] if "name" in kwargs else random_string()
    year = kwargs["year"] if "year" in kwargs else random.randint(2000, 2022)
    # build the feature
    feature = models.Feature()
    feature.name = name
    feature.year = year
    feature._path = fr"{config.SQL_LIBRARY_PATH}\Movies\Active\{name[0]}\{name} - {year}.mp4"
    feature._size = 0
    feature.status = 2  # active I think
    feature.play_count = 0
    feature.rating = 1
    feature._release_month = random.randint(1, 12)
    feature._release_year = year
    feature.created_at = datetime.now()
    feature.updated_at = datetime.now()
    db_session.add(feature)
    db_session.commit()
    db_session.refresh(feature)
    return feature


def random_playlist_item(db_session, **kwargs):
    feature_id = kwargs["feature_id"] if "feature_id" in kwargs else None
    content_type = models.ContentType.Feature.value  # feature
    start = kwargs["start"] if "start" in kwargs else datetime.now()
    duration = kwargs["duration"] if "duration" in kwargs else 60 * random.randint(90, 180)
    end = start + timedelta(seconds=duration)
    # build the playlist item
    playlist_item = models.Playlist()
    playlist_item.feature_id = feature_id
    playlist_item._content_type = content_type
    playlist_item.server_id = config.SERVER_ID
    playlist_item.start = start
    playlist_item.end = end
    db_session.add(playlist_item)
    db_session.commit()
    db_session.refresh(playlist_item)
    return playlist_item
