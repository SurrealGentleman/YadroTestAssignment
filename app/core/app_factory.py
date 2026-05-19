from typing import Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.api.routes import health, pages
from app.core.config import Settings, settings
from app.core.events import create_startup_handler
from app.db.session import SessionLocal, engine
from app.services.random_data_client import RandomDataToolsClient


def create_app(
    *,
    app_settings: Settings = settings,
    db_engine: Engine = engine,
    session_local: sessionmaker = SessionLocal,
    api_client: Any | None = None,
) -> FastAPI:
    client = api_client or RandomDataToolsClient(app_settings.random_data_api_url)
    app = FastAPI(
        title=app_settings.app_name,
        debug=app_settings.debug,
    )

    app.state.api_client = client
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(health.router)
    app.include_router(pages.router)
    app.add_event_handler(
        "startup",
        create_startup_handler(
            settings=app_settings,
            engine=db_engine,
            session_local=session_local,
            api_client=client,
        ),
    )
    return app
