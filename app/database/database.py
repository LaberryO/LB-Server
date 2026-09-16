from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.settings import settings

engine = create_engine(
    settings.db_url,
    pool_recycle=3600,
    echo=settings.debug_mode
)

_SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = _SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()