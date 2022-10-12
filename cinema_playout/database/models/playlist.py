from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, and_, select

from cinema_playout.config import SERVER_ID

from .base import Base


class Playlist(Base):
    __tablename__ = "Playlists"

    _id = Column("ContentID", Integer(), primary_key=True)
    feature_id = Column("FeatureID", Integer(), nullable=True)
    ad_id = Column("AdID", Integer(), nullable=True)
    filler_id = Column("FillerID", Integer(), nullable=True)
    preview_id = Column("PreviewID", Integer(), nullable=True)
    _content_type = Column("ContentType", Integer(), nullable=False)
    server_id = Column("ServerID", Integer(), nullable=False)
    start = Column("ContentStart", DateTime(), nullable=False)
    end = Column("ContentEnd", DateTime(), nullable=False)

    def __str__(self):
        return f"{self.content_type}:{self.content_id}:{self.server_id}:{self.start}"

    @property
    def content_type(self):
        return {
            0: "Feature",
            1: "Ad",
            2: "Preview",
            3: "Filler",
        }[self._content_type]

    @property
    def content_id(self):
        return {
            0: self.feature_id,
            1: self.ad_id,
            2: self.preview_id,
            3: self.filler_id,
        }[self._content_type]

    @classmethod
    def get_item_at(
        cls,
        db_session,
        start: datetime,
        server_id: int = SERVER_ID,
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
        content_type: int = None,
        server_id: int = SERVER_ID,
    ):
        query = select(cls).filter(cls.server_id == server_id).filter(cls.start > start)
        if content_type is not None:
            query = query.filter(cls._content_type == content_type)
        query = query.order_by(cls.start.asc()).limit(1)
        return db_session.execute(query).scalars().first()

    @classmethod
    def get_between(
        cls,
        db_session,
        start: datetime,
        end: datetime = None,
        server_id: int = SERVER_ID,
    ):
        query = select(cls).filter(cls.end > start)
        if end:
            query = query.filter(cls.start < end)
        if server_id:
            query = query.filter(cls.server_id == server_id)
        query = query.order_by(cls.start.asc())
        return db_session.execute(query).scalars().all()
