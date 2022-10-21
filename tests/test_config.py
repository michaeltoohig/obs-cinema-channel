from cinema_playout import config
from cinema_playout.database.session import Session


def test_config_values():
    assert config.DEBUG == False
    assert config.SERVER_ID == "0"
    assert config.DATABASE_URI == "sqlite://"
    assert config.REMOTE_LIBRARY_PATH != "replace-in-test"
    assert config.LOCAL_LIBRARY_PATH != "replace-in-test"
    assert config.OBS_LIBRARY_PATH == "replace-in-test"


def test_sqlalchemy_test_config():
    with Session() as session:
        assert str(session.bind.url) == "sqlite://"
