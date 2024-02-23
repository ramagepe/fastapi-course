from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import EmailStr
from sqlmodel import SQLModel


class PostBase(SQLModel):
    title: str
    content: str
    published: bool


class PostFull(PostBase):
    id: UUID
    created_at: datetime


class UserCreateRequest(SQLModel):
    email: EmailStr
    password: str


class UserCreateResponse(SQLModel):
    id: UUID
    email: EmailStr


class UserNoPassword(SQLModel):
    id: UUID
    email: EmailStr
    created_at: datetime


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class Token(SQLModel):
    token: str
    token_type: str


class TokenData(SQLModel):
    id: Optional[str] = None
