from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cinema_playout.config import DATABASE_URI

engine = create_engine(DATABASE_URI)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)
