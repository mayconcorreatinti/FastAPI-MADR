from http import HTTPStatus
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tcc_my_project.database import get_session
from tcc_my_project.models import User
from tcc_my_project.schemas import PublicCredentials, Token, credentials, message
from tcc_my_project.security import authenticated_user, get_token, hash, verify_password


app = FastAPI()

@app.post("/account", response_model=PublicCredentials,status_code=HTTPStatus.CREATED)
def create_account(account: credentials,session: Session = Depends(get_session)):
    user = session.scalar(
        Select(User).where(
            (account.username == User.username) | (account.email == User.email)
        )
    )

    if user:
        if user.username == account.username:
            raise HTTPException(
                detail="This name already exists!",
                status_code=HTTPStatus.CONFLICT,
            )

        elif user.email == account.email:
            raise HTTPException(
                detail="This email already exists!",
                status_code=HTTPStatus.CONFLICT,
            )

    response = User(
        username=account.username,
        email=account.email,
        password=hash(account.password),
    )

    session.add(response)
    session.commit()
    session.refresh(response)
    return response


@app.put("/account/{id}", response_model=PublicCredentials)
def change_account(id: int,account: credentials,session: Session = Depends(get_session),user=Depends(authenticated_user)):
    if id != user.id:
        raise HTTPException(
            detail="unauthorized request", status_code=HTTPStatus.UNAUTHORIZED
        )

    response = session.scalar(Select(User).where(User.id == id))

    try:
        response.username = account.username
        response.email = account.email
        response.password = hash(account.password)

        session.add(response)
        session.commit()
        session.refresh(response)
    except IntegrityError:
        raise HTTPException(
            detail="Username or email already exists!", status_code=HTTPStatus.CONFLICT
        )

    return response


@app.delete("/account/{id}", response_model=message)
def delete_account(id: int, session: Session = Depends(get_session), user=Depends(authenticated_user)):
    if id != user.id:
        raise HTTPException(
            detail="unauthorized request", status_code=HTTPStatus.UNAUTHORIZED
        )

    response = session.scalar(Select(User).where(User.id == id))

    session.delete(response)
    session.commit()

    return {"message": "User deleted!"}


@app.post("/token", status_code=HTTPStatus.CREATED, response_model=Token)
def create_token(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    response = session.scalar(Select(User).where(User.email == data.username))

    if response is None:
        raise HTTPException(
            detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
        )

    if not verify_password(data.password, response.password):
        raise HTTPException(
            detail="Incorrect username or password!", status_code=HTTPStatus.FORBIDDEN
        )

    token = get_token(data={"email": response.email})

    return {"access_token": token, "token_type": "bearer"}


@app.post("/refresh-token", status_code=HTTPStatus.CREATED, response_model=Token)
def refresh_token(user=Depends(authenticated_user)):
    token = get_token(data={"email": user.email})

    return {"access_token": token, "token_type": "bearer"}
