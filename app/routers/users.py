from typing import Annotated
from fastapi import Depends, status, APIRouter
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from uuid import UUID

from ..db import engine
from ..utils.handlers import not_found_exception
from ..utils.crypto import hash_password
from ..models import User
from ..schemas import UserCreateRequest, UserCreateResponse, UserNoPassword
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("")
def get_users(current_user: Annotated[User, Depends(get_current_user)]) -> list[User]:
    with Session(engine) as session:
        users = session.exec(
            select(User)).all()
    return users


@router.get("/{id}")
def get_user(id: UUID, current_user: Annotated[User, Depends(get_current_user)]) -> UserNoPassword:
    with Session(engine) as session:
        try:
            user = session.exec(
                select(User).where(User.id == id)).one()
        except NoResultFound:
            not_found_exception()
    return user


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserCreateRequest) -> UserCreateResponse:
    with Session(engine) as session:
        new_user.password = hash_password(new_user.password)
        user = User(**new_user.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
