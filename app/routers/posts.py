from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from uuid import UUID
from ..db import engine
from ..models import Post, User
from ..schemas import PostBase
from ..utils.handlers import forbidden_exception, not_found_exception
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("", dependencies=[Depends(get_current_user)])
def get_posts() -> list[Post]:
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()
    return posts


@router.get("/{id}", dependencies=[Depends(get_current_user)])
def get_post(id: UUID, current_user: Annotated[User, Depends(get_current_user)]) -> PostBase:
    with Session(engine) as session:
        try:
            post = session.exec(
                select(Post).where(Post.id == id)).one()
        except NoResultFound:
            not_found_exception()
    return post


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post, current_user: Annotated[User, Depends(get_current_user)]) -> Post:
    with Session(engine) as session:
        post = Post(user_id=current_user.id, **new_post.model_dump())
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: UUID, current_user: Annotated[User, Depends(get_current_user)]):
    with Session(engine) as session:
        try:
            post = session.exec(
                select(Post).where(Post.id == id)).one()
            if post.user_id != current_user.id:
                forbidden_exception()
            session.delete(post)
            session.commit()
        except NoResultFound:
            not_found_exception()


@router.put("/{id}", status_code=status.HTTP_201_CREATED)
def update_post(updated_post: Post, id: UUID, current_user: Annotated[User, Depends(get_current_user)]) -> PostBase:
    with Session(engine) as session:
        try:
            post = session.exec(
                select(Post).where(Post.id == id)).one()
            if post.user_id != current_user.id:
                forbidden_exception()
            post.title = updated_post.title
            post.content = updated_post.content
            post.published = updated_post.published
            session.add(post)
            session.commit()
            session.refresh(post)
        except NoResultFound:
            not_found_exception()
    return post
