from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from uuid import UUID
from ..db import engine
from ..models import Post
from ..schemas import PostBase
from ..utils.handlers import not_found_exception
from ..oauth2 import verify_token


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("", dependencies=[Depends(verify_token)])
def get_posts() -> list[Post]:
    with Session(engine) as session:
        posts = session.exec(select(Post)).all()
    return posts


@router.get("/{id}", dependencies=[Depends(verify_token)])
def get_post(id: UUID) -> PostBase:
    with Session(engine) as session:
        try:
            post = session.exec(
                select(Post).where(Post.id == id)).one()
        except NoResultFound:
            not_found_exception()
    return post


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
def create_post(new_post: Post) -> Post:
    with Session(engine) as session:
        post = Post(**new_post.model_dump())
        session.add(post)
        session.commit()
        session.refresh(post)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_token)])
def delete_post(id: UUID):
    with Session(engine) as session:
        try:
            post = session.exec(
                select(Post).where(Post.id == id)).one()
            session.delete(post)
            session.commit()
        except NoResultFound:
            not_found_exception()


@router.put("/{id}", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
def update_post(updated_post: Post, id: UUID) -> PostBase:
    with Session(engine) as session:
        try:
            post = session.exec(
                select(Post).where(Post.id == id)).one()
            post.title = updated_post.title
            post.content = updated_post.content
            post.published = updated_post.published
            session.add(post)
            session.commit()
            session.refresh(post)
        except NoResultFound:
            not_found_exception()
    return post
