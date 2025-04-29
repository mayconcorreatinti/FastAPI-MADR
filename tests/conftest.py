import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from tcc_my_project.database import get_session
from tcc_my_project.models import User, table_registry,Books
from tcc_my_project.app import app
from tcc_my_project.security import hash


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
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
    user = User(username="string",email="user@example.com",password=hash("string"))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clear_password = "string"

    return user


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
def bookdb(session):
    book=Books(
        year= 1900,
        title= "livro do heroi",
        novelist_id= 2
    )
    session.add(book)
    session.commit()
    session.refresh(book)

    return book