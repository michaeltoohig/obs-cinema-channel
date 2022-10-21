import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from cinema_playout import config
from cinema_playout.database.models.base import Base


@pytest.fixture(autouse=True, scope="session")
def setup_mock_storage(tmp_path_factory):
    config.REMOTE_LIBRARY_PATH = str(tmp_path_factory.mktemp("remote"))
    config.LOCAL_LIBRARY_PATH = str(tmp_path_factory.mktemp("local"))


@pytest.fixture(scope="session")
def connection():
    engine = create_engine("sqlite://")
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()

    # seed_database()

    yield

    Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))
    transaction.rollback()
