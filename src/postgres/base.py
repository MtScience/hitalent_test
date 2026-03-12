from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import config


class Base(DeclarativeBase):
    pass


engine = create_engine(config.POSTGRES_URL, echo=True)
async_session = sessionmaker(
    class_=Session,
    bind=engine,
)


def get_async_session() -> Generator[Session, None]:
    with async_session() as session, session.begin():
        yield session
