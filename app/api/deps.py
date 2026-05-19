from collections.abc import Generator

from fastapi import Request
from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_api_client(request: Request):
    return request.app.state.api_client
