from collections.abc import Callable, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.core.app_factory import create_app
from app.core.config import settings
from app.db.base import Base
from app.services import people as people_service

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class FakeApiClient:
    def fetch_people(self, count: int) -> list[dict[str, object]]:
        return [
            {
                "Gender": "Женщина",
                "FirstName": f"Имя{i}",
                "LastName": f"Фамилия{i}",
                "Phone": f"+7 900 000-00-{i:02d}",
                "Email": f"user{i}@example.test",
                "Address": f"Город, улица {i}",
            }
            for i in range(1, count + 1)
        ]


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def fake_api_client() -> FakeApiClient:
    return FakeApiClient()


@pytest.fixture
def app(fake_api_client: FakeApiClient) -> FastAPI:
    test_settings = settings.model_copy(update={"skip_initial_load": True})
    app = create_app(
        app_settings=test_settings,
        db_engine=engine,
        session_local=TestingSessionLocal,
        api_client=fake_api_client,
    )
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture(autouse=True)
def prepare_database(app: FastAPI) -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db() -> Generator[Session, None, None]:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def startup_client(fake_api_client: FakeApiClient) -> Generator[TestClient, None, None]:
    test_settings = settings.model_copy(
        update={
            "skip_initial_load": False,
            "initial_load_count": 3,
        }
    )
    app = create_app(
        app_settings=test_settings,
        db_engine=engine,
        session_local=TestingSessionLocal,
        api_client=fake_api_client,
    )
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.drop_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_people(fake_api_client: FakeApiClient) -> Callable[[int], None]:
    def _create_people(count: int = 1) -> None:
        with TestingSessionLocal() as db:
            people_service.load_people(
                db=db,
                api_client=fake_api_client,
                count=count,
            )

    return _create_people
