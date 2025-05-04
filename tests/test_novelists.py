from http import HTTPStatus


def test_create_novelists(client,token):
    response=client.post(
        "novelists",json={
            "name":"test"
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id":1,
        "name":"test"
    }


def test_create_novelists_error_name(client,novelistdb,token):
    response=client.post(
        "novelists",json={
            "name":novelistdb.name
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail":"This name already exists in novelists!"}


def test_delete_novelist(client,novelistdb,token):
    response=client.delete(
        f"novelists/{novelistdb.id}",headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message":"Novelist deleted from MADR"}


def test_delete_novelist_error_not_found(client,novelistdb,token):
    response=client.delete(
        f"novelists/{novelistdb.id + 1}",headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"Novelist not listed in MADR"}


def test_update_novelist(client,novelistdb,token):
    response=client.patch(
        f"novelists/{novelistdb.id}",json={
           "name": "testtest"
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id":1,
        "name": "testtest"
    }


def test_update_novelist_error_not_found(client,novelistdb,token):
    response=client.patch(
        f"novelists/{novelistdb.id + 1}",json={
            "name":"testtest"
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"Novelist not listed in MADR"}


def test_update_novelist_error_name(client,novelistdb,novelistdb2,token):
    response=client.patch(
        f"novelists/{novelistdb.id}",json={
            "name":novelistdb2.name
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail":"This name already exists in novelists!"}


def test_get_novelist(client,novelistdb):
    response=client.get(
        f"novelists/{novelistdb.id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id":1,
        "name":"test"
    }


def test_get_novelist_error_not_found(client,novelistdb):
    response=client.get(
        f"novelists/{novelistdb.id + 1}"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"Novelist not listed in MADR"}


def test_t_novelist_filter(client,novelistdb):
    response=client.get(
        "novelists?name=tes&limit=1"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "novelists":[
            {
                "id":1,
                "name":"test"
            }
        ]
    }