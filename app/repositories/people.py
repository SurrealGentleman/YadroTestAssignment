from collections.abc import Iterable

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.person import Person


def add_many(db: Session, people: Iterable[Person]) -> int:
    models = list(people)
    if not models:
        return 0

    db.add_all(models)
    db.commit()
    return len(models)


def count(db: Session) -> int:
    return db.scalar(select(func.count(Person.id))) or 0


def list_people(db: Session, page: int, per_page: int) -> tuple[list[Person], int]:
    total = count(db)
    offset = (page - 1) * per_page
    people = list(
        db.scalars(
            select(Person).order_by(Person.id.desc()).offset(offset).limit(per_page)
        )
    )
    return people, total


def get_by_id(db: Session, person_id: int) -> Person | None:
    return db.get(Person, person_id)


def get_random(db: Session) -> Person | None:
    return db.scalar(select(Person).order_by(func.random()).limit(1))
