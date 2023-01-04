from pathlib import Path, PureWindowsPath

from sqlalchemy import Column, DateTime, Float, Integer, String, select

from cinema_playout import config
from cinema_playout.database.models.base import Base


class PlaylistItem(object):
    @classmethod
    def get_by_id(cls, db_session, id):
        query = select(cls).filter(cls.id == id)
        return db_session.execute(query).scalars().one()

    @property
    def path(self) -> PureWindowsPath:
        return PureWindowsPath(self._path)

    @property
    def remote_path(self) -> Path:
        relative = self.path.relative_to(config.SQL_LIBRARY_PATH)
        return Path(config.REMOTE_LIBRARY_PATH) / relative

    @property
    def local_path(self) -> Path:
        relative = self.path.relative_to(config.SQL_LIBRARY_PATH)
        return Path(config.LOCAL_LIBRARY_PATH) / relative


class Feature(Base, PlaylistItem):
    __tablename__ = "Features"

    id = Column("FeatureID", Integer(), primary_key=True)
    name = Column("FeatureName", String(), nullable=False)
    year = Column("FeatureYear", Integer(), nullable=True)
    _path = Column("FeaturePath", String(), nullable=False)
    _size = Column("FeatureSize", Integer(), nullable=False)
    status = Column("FeatureStatus", Integer(), nullable=False)
    play_count = Column("FeaturePlayCount", Integer(), nullable=False)
    rating = Column("FeatureIMDBRating", Float(), nullable=True)
    _release_month = Column("FeatureReleasedMM", Integer(), nullable=True)
    _release_year = Column("FeatureReleasedYY", Integer(), nullable=True)
    released_at = Column("FeatureReleased", DateTime(), nullable=True)
    created_at = Column("FeatureCreated", DateTime(), nullable=False)
    updated_at = Column("FeatureUpdated", DateTime(), nullable=False)

    def __str__(self):
        if self.year is None:
            return self.name
        else:
            return f"{self.name} ({self.year})"


# class Advertisement(Base, PlaylistItem):
#     __tablename__ = "Advertisements"


# class Preview(Base, PlaylistItem):
#     __tablename__ = "Previews"


# class Filler(Base, PlaylistItem):
#     __tablename__ = "Fillers"
