from typing import Annotated, Optional
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from uuid import UUID
from ..db import get_session
from ..models import Post, User
from ..schemas import PostIn, PostOutBase, PostOutFull
from ..utils.handlers import forbidden_exception, not_found_exception
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("", dependencies=[Depends(get_current_user)])
def get_posts(
        limit: int = 10,
        skip: int = 0,
        search: Optional[str] = "",
        session: Session = Depends(get_session)) -> list[PostOutFull]:
    posts = session.exec(
        select(Post)
        .options(joinedload(Post.user))
        .limit(limit)
        .offset(skip)
        .filter(func.lower(Post.title).contains(func.lower(search)))).all()
    return posts


@router.get("/{id}", dependencies=[Depends(get_current_user)])
def get_post(
        id: UUID,
        session: Session = Depends(get_session)) -> PostOutBase:
    try:
        post = session.exec(
            select(Post)
            .where(Post.id == id)
            .options(joinedload(Post.user))).one()
    except NoResultFound:
        not_found_exception()
    return post


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(
        new_post: PostIn,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)) -> PostOutFull:
    post = Post(user_id=current_user.id, **new_post.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
        id: UUID,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)):
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
def update_post(
        updated_post: Post, id: UUID,
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)) -> PostOutBase:
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
