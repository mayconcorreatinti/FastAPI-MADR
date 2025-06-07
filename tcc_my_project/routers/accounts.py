from http import HTTPStatus
from fastapi import Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from tcc_my_project.database import get_session
from tcc_my_project.models import User
from tcc_my_project.schemas import PublicCredentials, Token, Credentials, Message
from tcc_my_project.security import authenticated_user, get_token, hash, verify_password


router = APIRouter(tags=["accounts"],prefix="/accounts")

@router.post("/", response_model=PublicCredentials,status_code=HTTPStatus.CREATED)
async def create_account(
    account: Credentials,
    session: AsyncSession = Depends(get_session)
):
    user = await session.scalar(
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
    await session.commit()
    await session.refresh(response)
    return response


@router.put("/{id}", response_model=PublicCredentials)
async def change_account(
    id: int,
    account: Credentials,
    session: AsyncSession = Depends(get_session),
    user=Depends(authenticated_user)
):
    if id != user.id:
        raise HTTPException(
            detail="unauthorized request", status_code=HTTPStatus.UNAUTHORIZED
        )

    response = await session.scalar(Select(User).where(User.id == id))
    
    try:
        response.username = account.username
        response.email = account.email
        response.password = hash(account.password)


        await session.commit()
        await session.refresh(response)

    except IntegrityError:
        raise HTTPException(
            detail="Username or email already exists!", status_code=HTTPStatus.CONFLICT
        )

    return response


@router.delete("/{id}", response_model=Message)
async def delete_account(
    id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(authenticated_user)
):
    if id != user.id:
        raise HTTPException(
            detail="unauthorized request", status_code=HTTPStatus.UNAUTHORIZED
        )

    response = await session.scalar(Select(User).where(User.id == id))

    session.delete(response)
    await session.commit()

    return {"message": "User deleted!"}


@router.post("/token", status_code=HTTPStatus.CREATED, response_model=Token)
async def create_token(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    response = await session.scalar(Select(User).where(User.email == data.username))

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


@router.post("/refresh-token", status_code=HTTPStatus.CREATED, response_model=Token)
def refresh_token(
    user=Depends(authenticated_user)
):
    token = get_token(data={"email": user.email})

    return {"access_token": token, "token_type": "bearer"}
