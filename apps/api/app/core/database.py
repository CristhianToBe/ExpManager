from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from .config import get_settings


class Base(DeclarativeBase):
    pass


_engine = create_engine(get_settings().default_sqlite_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)


def configure_database(sqlite_url: str) -> None:
    global _engine, SessionLocal
    _engine.dispose()
    _engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    SessionLocal.configure(bind=_engine)


def get_engine():
    return _engine


def create_all() -> None:
    from app.models import audit, profile, workspace  # noqa: F401
    Base.metadata.create_all(bind=_engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
