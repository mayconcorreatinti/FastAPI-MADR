import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from testcontainers.postgres import PostgresContainer # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from tcc_my_project.database import get_session
from tcc_my_project.models import User, table_registry,Books,Novelist
from tcc_my_project.app import app
from tcc_my_project.security import hash
import factory # type: ignore
import sys
import asyncio


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    
class UserFactory(factory.Factory):
    class Meta:
        model = User  

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


@pytest_asyncio.fixture
async def session():
    #raising the postgres container, waiting for it to start 
    # and using it for testing
    with PostgresContainer('postgres:16',driver='psycopg') as postgres: 
        engine = create_async_engine(postgres.get_connection_url()) 

        async with engine.begin() as conn: 
            await conn.run_sync(table_registry.metadata.create_all) 

        async with AsyncSession(engine, expire_on_commit=False) as session:
            yield session

        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user(session):
    password="string"
    user = UserFactory(password=hash(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    user.clear_password = password

    return user


@pytest_asyncio.fixture
async def user2(session):
    password="string"
    user2 = UserFactory(password=hash(password))
    session.add(user2)
    await session.commit()
    await session.refresh(user2)
    user2.clear_password = password

    return user2


@pytest.fixture
def token(client, user):
    response = client.post(
        "accounts/token", data={
            "username": user.email, 
            "password": user.clear_password
        }
    )

    return response.json()["access_token"]


@pytest_asyncio.fixture
async def novelistdb(session):
    novelist=Novelist(
        name= "test"
    )
    session.add(novelist)
    await session.commit()
    await session.refresh(novelist)

    return novelist


@pytest_asyncio.fixture
async def novelistdb2(session):
    novelist2=Novelist(
        name= "test2"
    )
    session.add(novelist2)
    await session.commit()
    await session.refresh(novelist2)

    return novelist2


@pytest_asyncio.fixture
async def bookdb(session,novelistdb):
    book=Books(
        year= 1900,
        title= "book test",
        novelist_id= novelistdb.id
    )
    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book


@pytest_asyncio.fixture
async def bookdb2(session,novelistdb):
    book2=Books(
        year= 1901,
        title= "book test2",
        novelist_id= novelistdb.id
    )
    session.add(book2)
    await session.commit()
    await session.refresh(book2)

    return book2

