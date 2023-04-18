import pytest
import pytest_structlog
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from cinema_playout import config
from cinema_playout.database.models.base import Base


@pytest.fixture(autouse=True, scope="function")
def setup_mock_storage(tmp_path_factory):
    remote = tmp_path_factory.mktemp("remote")
    config.REMOTE_LIBRARY_PATH = str(remote)
    config.REMOTE_HOLD_ROOT_PATH = str(remote / f"CinemaPlayout/server-{config.SERVER_ID}")
    config.REMOTE_HOLD_VIDEO_PATH = str(
        remote / f"CinemaPlayout/server-{config.SERVER_ID}/{config.DIRECTORY_HOLD_VIDEO}"
    )
    config.REMOTE_HOLD_MUSIC_PATH = str(
        remote / f"CinemaPlayout/server-{config.SERVER_ID}/{config.DIRECTORY_HOLD_MUSIC}"
    )
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
