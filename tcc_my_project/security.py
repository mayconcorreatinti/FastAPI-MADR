from datetime import UTC, datetime, timedelta
from http import HTTPStatus
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash  # type: ignore
from sqlalchemy import Select
from tcc_my_project.database import get_session
from tcc_my_project.models import User
from tcc_my_project.settings import Settings


password_hash = PasswordHash.recommended()
token_ = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()


def hash(password: str):
    return password_hash.hash(password)


def verify_password(password, hash):
    return password_hash.verify(password, hash)


def get_token(data: dict):
    exp = datetime.now(UTC) + timedelta(minutes=settings.TOKEN_TIME)
    sub = data.copy()
    payload = {"sub": sub["email"], "exp": exp}
    token = jwt.encode(payload,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return token


def authenticated_user(token: str = Depends(token_),session=Depends(get_session)):
    try:
        user = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        payload = user.get("sub")

        if not payload:
            raise HTTPException(
                detail="Unable to validate credentials!",
                status_code=HTTPStatus.UNAUTHORIZED,
            )

    except jwt.DecodeError:
        raise HTTPException(
            detail="Unable to validate credentials!",
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    authenticated_user = session.scalar(Select(User).where(User.email == payload))

    if not authenticated_user:
        raise HTTPException(
            detail="Unable to validate credentials!",
            status_code=HTTPStatus.UNAUTHORIZED,
        )
    return authenticated_user
