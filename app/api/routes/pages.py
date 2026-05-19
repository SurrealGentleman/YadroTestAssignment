import math

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.api.deps import get_api_client, get_db
from app.services import people as people_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    page: int = 1,
    per_page: int = 50,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    page = max(page, 1)
    per_page = min(max(per_page, 1), 200)
    people, total = people_service.list_people(db=db, page=page, per_page=per_page)
    pages = max(math.ceil(total / per_page), 1)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "people": people,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
        },
    )


@router.post("/load")
def load_people(
    count: int = Form(...),
    db: Session = Depends(get_db),
    api_client=Depends(get_api_client),
) -> RedirectResponse:
    people_service.load_people(db=db, api_client=api_client, count=count)
    return RedirectResponse("/", status_code=303)


@router.get("/random", response_class=HTMLResponse)
def random_person(
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    person = people_service.get_random_person(db=db)
    if person is None:
        raise HTTPException(status_code=404, detail="В базе пока нет пользователей")

    return templates.TemplateResponse(
        request,
        "person.html",
        {"person": person, "title": "Случайный пользователь"},
    )


@router.get("/{person_id:int}", response_class=HTMLResponse)
def person_page(
    person_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    person = people_service.get_person(db=db, person_id=person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return templates.TemplateResponse(
        request,
        "person.html",
        {"person": person, "title": f"{person.first_name} {person.last_name}"},
    )
