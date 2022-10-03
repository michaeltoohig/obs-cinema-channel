from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str

    def save(self, db_session):
        """
        :param db_session:
        :return:
        """
        try:
            db_session.add(self)
            return db_session.commit()
        except SQLAlchemyError as exc:
            db_session.rollback()
            raise exc  # TODO replace with proper exception handling

    def delete(self, db_session):
        """
        :param db_session:
        :return:
        """
        try:
            db_session.delete(self)
            db_session.commit()
            return True
        except SQLAlchemyError as exc:
            raise exc  # TODO replace with proper exception handling

    def update(self, db_session, **kwargs):
        """
        :param db_session:
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save(db_session)
