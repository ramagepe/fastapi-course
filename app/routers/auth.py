from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..schemas import Token
from ..db import engine
from ..models import User
from ..utils.handlers import unauthorized_exception
from ..utils.crypto import verify_password
from ..oauth2 import create_token

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends()) -> Token:
    access_token = None
    with Session(engine) as session:
        user = session.exec(select(User).where(
            User.email == user_credentials.username)).first()
        if not user or not verify_password(user_credentials.password, user.password):
            unauthorized_exception()
        access_token = create_token(data={"user_id": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")
