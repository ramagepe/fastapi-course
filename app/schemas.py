from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import EmailStr
from sqlmodel import SQLModel


class UserCreateRequest(SQLModel):
    email: EmailStr
    password: str


class UserOut(SQLModel):
    id: UUID
    email: str


class UserNoPassword(SQLModel):
    id: UUID
    email: EmailStr
    created_at: datetime


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    id: Optional[str] = None


class PostOutBase(SQLModel):
    title: str
    content: str
    published: bool
    user: UserOut


class PostOutFull(PostOutBase):
    id: UUID
    created_at: datetime


class PostIn(SQLModel):
    title: str
    content: str
    published: bool = True
