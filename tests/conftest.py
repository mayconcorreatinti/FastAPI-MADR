import pytest
from testcontainers.postgres import PostgresContainer # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from tcc_my_project.database import get_session
from tcc_my_project.models import User, table_registry,Books,Novelist
from tcc_my_project.app import app
from tcc_my_project.security import hash
import factory # type: ignore


class UserFactory(factory.Factory):
    class Meta:
        model = User  

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


@pytest.fixture(scope='session')
def engine():
    #raising the postgres container, waiting for it to start 
    # and using it for testing
    with PostgresContainer('postgres:16',driver='psycopg') as postgres: 
        _engine = create_engine(postgres.get_connection_url()) 

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    password="string"
    user = UserFactory(password=hash(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clear_password = password

    return user


@pytest.fixture
def user2(session):
    password="string"
    user2 = UserFactory(password=hash(password))
    session.add(user2)
    session.commit()
    session.refresh(user2)
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


@pytest.fixture
def novelistdb(session):
    novelist=Novelist(
        name= "test"
    )
    session.add(novelist)
    session.commit()
    session.refresh(novelist)

    return novelist


@pytest.fixture
def novelistdb2(session):
    novelist2=Novelist(
        name= "test2"
    )
    session.add(novelist2)
    session.commit()
    session.refresh(novelist2)

    return novelist2


@pytest.fixture
def bookdb(session,novelistdb):
    book=Books(
        year= 1900,
        title= "book test",
        novelist_id= novelistdb.id
    )
    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@pytest.fixture
def bookdb2(session,novelistdb):
    book2=Books(
        year= 1901,
        title= "book test2",
        novelist_id= novelistdb.id
    )
    session.add(book2)
    session.commit()
    session.refresh(book2)

    return book2

