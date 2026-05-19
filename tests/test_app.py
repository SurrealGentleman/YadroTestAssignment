from collections.abc import Callable

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.repositories import people as people_repository
from app.services import people as people_service


class CappedApiClient:
    def __init__(self, max_batch_size: int = 100) -> None:
        self.max_batch_size = max_batch_size
        self.calls = 0

    def fetch_people(self, count: int) -> list[dict[str, object]]:
        self.calls += 1
        batch_size = min(count, self.max_batch_size)
        return [
            {
                "Gender": "Мужчина",
                "FirstName": f"Имя{self.calls}_{i}",
                "LastName": "Тестов",
                "Phone": "+7 900 000-00-00",
                "Email": f"user{self.calls}_{i}@example.test",
                "Address": "Город",
            }
            for i in range(batch_size)
        ]


def test_startup_loads_initial_people(startup_client: TestClient) -> None:
    response = startup_client.get("/")

    assert response.status_code == 200
    assert "Всего записей: 3" in response.text
    assert "Имя1" in response.text


def test_load_people_from_form(client: TestClient) -> None:
    response = client.post("/load", data={"count": 2}, follow_redirects=True)

    assert response.status_code == 200
    assert "Всего записей: 2" in response.text
    assert "user2@example.test" in response.text


def test_person_page_by_id(
    client: TestClient,
    create_people: Callable[[int], None],
) -> None:
    create_people(1)

    response = client.get("/1")

    assert response.status_code == 200
    assert "Имя1" in response.text
    assert "Город, улица 1" in response.text


def test_random_person_returns_existing_person(
    client: TestClient,
    create_people: Callable[[int], None],
) -> None:
    create_people(2)

    response = client.get("/random")

    assert response.status_code == 200
    assert "Случайный пользователь" in response.text
    assert "user" in response.text


def test_people_table_is_paginated(
    client: TestClient,
    create_people: Callable[[int], None],
) -> None:
    create_people(3)

    response = client.get("/?page=1&per_page=2")

    assert response.status_code == 200
    assert "Страница 1 из 2" in response.text


def test_load_people_fetches_until_requested_count(db: Session) -> None:
    api_client = CappedApiClient(max_batch_size=100)

    created_count = people_service.load_people(
        db=db,
        api_client=api_client,
        count=250,
    )

    assert created_count == 250
    assert people_repository.count(db) == 250
    assert api_client.calls == 3
