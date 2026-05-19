import json
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.person import Person
from app.repositories import people as people_repository


def load_initial_people(db: Session, api_client: Any, count: int) -> int:
    if people_repository.count(db) > 0:
        return 0
    return load_people(db=db, api_client=api_client, count=count)


def load_people(db: Session, api_client: Any, count: int) -> int:
    if count < 1:
        raise HTTPException(status_code=400, detail="Количество должно быть больше нуля")
    if count > 100_000:
        raise HTTPException(status_code=400, detail="Слишком большое значение")

    raw_people = _fetch_people_until_count(api_client=api_client, count=count)
    return people_repository.add_many(
        db=db,
        people=(_normalize_person(person) for person in raw_people),
    )


def list_people(db: Session, page: int, per_page: int) -> tuple[list[Person], int]:
    return people_repository.list_people(db=db, page=page, per_page=per_page)


def get_person(db: Session, person_id: int) -> Person | None:
    return people_repository.get_by_id(db=db, person_id=person_id)


def get_random_person(db: Session) -> Person | None:
    return people_repository.get_random(db=db)


def _normalize_person(data: dict[str, Any]) -> Person:
    return Person(
        gender=str(data.get("Gender") or data.get("gender") or ""),
        first_name=str(data.get("FirstName") or data.get("first_name") or ""),
        last_name=str(data.get("LastName") or data.get("last_name") or ""),
        phone=str(data.get("Phone") or data.get("phone") or ""),
        email=str(data.get("Email") or data.get("email") or ""),
        address=str(data.get("Address") or data.get("address") or ""),
        raw_data=json.dumps(data, ensure_ascii=False),
    )


def _fetch_people_until_count(api_client: Any, count: int) -> list[dict[str, Any]]:
    people: list[dict[str, Any]] = []

    while len(people) < count:
        requested_count = count - len(people)
        batch = api_client.fetch_people(requested_count)
        if not batch:
            break

        remaining_count = count - len(people)
        people.extend(batch[:remaining_count])

    return people
