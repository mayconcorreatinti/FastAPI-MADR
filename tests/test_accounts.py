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


def test_username_error_with_post(client,user):
    response = client.post(
        "accounts",json={
            "username": user.username,
            "email": "user@example.com",
            "password": "string"
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail":"This name already exists!"}


def test_error_in_email_with_post(client,user):
    response = client.post(
        "accounts",json={
            "username": "string2",
            "email": user.email,
            "password": "string"
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail":"This email already exists!"}


def test_authorization_error_with_put(client,user,user2,token):
    response = client.put(
        f"accounts/{user2.id}",json={
            "username": "string3",
            "email": "string@string.com",
            "password": "string"
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail":"unauthorized request"}


def test_error_in_email_with_put(client,token,user,user2):
    response= client.put(
        f"accounts/{user.id}",json={
            "username": user2.username,
            "email": "testtest@gmail.com",
            "password": "string"
        },headers={"Authorization":f"bearer {token}"}
    )
   
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail":"Username or email already exists!"}


def test_error_delete_unauthorized(client,token,user2):
    response = client.delete(
        f"accounts/{user2.id}",headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail":"unauthorized request"}


def test_error_token_email(client,user):
    response=client.post(
        "accounts/token",data={
            "username":"fakeuser@gmail.com",
            "password":user.password
        }
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail":"Incorrect username or password!"}


def test_error_token_password(client,user):
    response=client.post(
        "accounts/token",data={
            "username":user.email,
            "password":"fakepassword123"
        }
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail":"Incorrect username or password!"}