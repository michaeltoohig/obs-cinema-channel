from datetime import datetime
from enum import IntEnum

from sqlalchemy import Column, DateTime, Integer, and_, select

from cinema_playout import config

from .base import Base


class ContentType(IntEnum):
    Feature = 0
    Ad = 1
    Preview = 2
    Filler = 3


class Playlist(Base):
    __tablename__ = "Playlists"

    id = Column("ContentID", Integer(), primary_key=True)
    feature_id = Column("FeatureID", Integer(), nullable=True)
    ad_id = Column("AdID", Integer(), nullable=True)
    filler_id = Column("FillerID", Integer(), nullable=True)
    preview_id = Column("PreviewID", Integer(), nullable=True)
    _content_type = Column("ContentType", Integer(), nullable=False)
    server_id = Column("ServerID", Integer(), nullable=False)
    start = Column("ContentStart", DateTime(), nullable=False)
    end = Column("ContentEnd", DateTime(), nullable=False)

    def __str__(self):
        return f"{self.content_type.name}:{self.content_id}:{self.server_id}:{self.start}"

    @property
    def content_type(self):
        return ContentType(self._content_type)

    @property
    def content_id(self):
        return {
            ContentType.Feature: self.feature_id,
            ContentType.Ad: self.ad_id,
            ContentType.Preview: self.preview_id,
            ContentType.Filler: self.filler_id,
        }[self.content_type]

    @classmethod
    def get_item_at(
        cls,
        db_session,
        start: datetime,
        server_id: int = config.SERVER_ID,
    ):
        query = (
            select(cls)
            .filter(cls.server_id == server_id)
            .filter(
                and_(
                    cls.start <= start,
                    cls.end > start,
                )
            )
        )
        return db_session.execute(query).scalars().first()

    @classmethod
    def get_next_item(
        cls,
        db_session,
        start: datetime,
        content_type: ContentType = None,
        server_id: int = config.SERVER_ID,
    ):
        query = select(cls).filter(cls.server_id == server_id).filter(cls.start > start)
        if content_type is not None:
            query = query.filter(cls._content_type == content_type.value)
        query = query.order_by(cls.start.asc()).limit(1)
        return db_session.execute(query).scalars().first()

    @classmethod
    def get_between(
        cls,
        db_session,
        start: datetime,
        end: datetime = None,
        server_id: int = config.SERVER_ID,
    ):
        query = select(cls).filter(cls.end > start)
        if end:
            query = query.filter(cls.start < end)
        if server_id:
            query = query.filter(cls.server_id == server_id)
        query = query.order_by(cls.start.asc())
        return db_session.execute(query).scalars().all()
