from sqlalchemy import Column, DateTime, Float, Integer, String, select

from cinema_playout.database.models.base import Base


class Feature(Base):
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

    # def get_path(self):
    #     local_root = Path(MEDIA_ROOT)
    #     relative_path = PureWindowsPath(self._path).relative_to("//10.0.0.126/media")
    #     return local_root / relative_path

    @classmethod
    def get_by_id(cls, db_session, id):
        query = select(cls).filter(cls.id == id)
        return db_session.execute(query).scalars().one()

    # @classmethod
    # def get_removed(cls, db_session):
    #     query = select(cls).filter(cls.status == 99)
    #     return db_session.execute(query).scalars().all()

    # @classmethod
    # def get_pending(cls, db_session, orderby: FeatureOrderBy = None):
    #     query = select(cls).filter(cls.status == 0)
    #     if orderby:
    #         query = query.order_by(getattr(cls, orderby.value))
    #     return db_session.execute(query).scalars().all()

    # @classmethod
    # def get_active(cls, db_session):
    #     query = select(cls).filter(cls.status == 1)
    #     return db_session.execute(query).scalars().all()
