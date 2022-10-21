from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cinema_playout import config

engine = create_engine(config.DATABASE_URI)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
