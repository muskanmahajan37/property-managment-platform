from typing import Any

from src.flex.db.session import SessionLocal


def get_db() -> Any:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
