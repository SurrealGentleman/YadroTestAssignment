from typing import Any, Callable

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.db.base import Base
from app.services import people as people_service


def create_startup_handler(
    *,
    settings: Settings,
    engine: Engine,
    session_local: sessionmaker,
    api_client: Any,
) -> Callable[[], None]:
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)
        if settings.skip_initial_load:
            return

        with session_local() as db:
            people_service.load_initial_people(
                db=db,
                api_client=api_client,
                count=settings.initial_load_count,
            )

    return on_startup
