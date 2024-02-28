from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import ForeignKey, text, Column, DateTime
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[UUID] = Field(default=text(
        "uuid_generate_v4()"), primary_key=True)
    email: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default=text(
        "now()"), sa_column=Column(DateTime(timezone=True)))
    posts: list["Post"] = Relationship(back_populates="user")


class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: Optional[UUID] = Field(default=text(
        "uuid_generate_v4()"), primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    created_at: datetime = Field(default=text(
        "now()"), sa_column=Column(DateTime(timezone=True)))
    user_id: UUID = Field(sa_column=Column(ForeignKey(
        "users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False))
    user: User = Relationship(back_populates="posts")


class Vote(SQLModel, table=True):
    __tablename__ = "votes"
    post_id: UUID = Field(sa_column=Column(ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True))
    user_id: UUID = Field(sa_column=Column(ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True))
