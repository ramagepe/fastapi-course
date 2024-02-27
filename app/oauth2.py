from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv

from .db import engine
from .schemas import TokenData
from .utils.handlers import unauthorized_exception
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    token_data = None
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id: str = payload.get("user_id")
        if not user_id:
            unauthorized_exception()
        token_data: str = TokenData(id=user_id)
    except JWTError:
        unauthorized_exception()
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        token = verify_token(token)
        user = session.exec(
            select(User)
            .where(User.id == token.id)
        ).first()
    return user
