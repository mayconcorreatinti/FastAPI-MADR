from http import HTTPStatus


def test_create_account(client):
    response = client.post(
        "/accounts",json={
            "username": "string",
            "email": "user@example.com",
            "password": "string"
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "string",
        "email": "user@example.com",
    }


def test_change_account(client, token, user):
    response = client.put(
        f"/accounts/{user.id}",json={
            "username": "testtest",
            "email": "testtest@example.com",
            "password": "string",
        },headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": user.id,
        "username": "testtest",
        "email": "testtest@example.com",
    }


def test_delete_account(client, token, user):
    response = client.delete(
        f"/accounts/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted!"}


def test_token(client, user):
    response = client.post(
        "accounts/token", data={
            "username": user.email, 
            "password": user.clear_password
        }
    )
    
    assert response.status_code == HTTPStatus.CREATED
    assert "access_token" in response.json()


def test_refresh_token(client, token):
    response = client.post(
        "accounts/refresh-token", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert "access_token" in response.json()
