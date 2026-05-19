from fastapi import FastAPI

from app.core import app_factory


def create_app() -> FastAPI:
    return app_factory.create_app()


app = create_app()
