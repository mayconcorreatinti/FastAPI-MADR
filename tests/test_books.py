from http import HTTPStatus


def test_create_book(client,token):
    response = client.post(
        "books",json={
            "year": 1900,
            "title": "booktest",
            "novelist_id": 23
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "year": 1900,
        "title": "booktest",
        "novelist_id": 23
    }


def test_create_book_error_title(client,bookdb,token):
    response = client.post(
        "books",json={
            "year": 1900,
            "title": bookdb.title,
            "novelist_id": 23
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail":"This title already exists!"}


def test_delete_book(client,token,bookdb):
    response = client.delete(
        f"books/{bookdb.id}",headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message":"Book deleted in MADR"} 


def test_delete_book_not_found(client,token,bookdb):
    response = client.delete(
        f"books/{bookdb.id + 1}",headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() ==  {"detail":"Book not listed in MADR"}


def test_patch_book(client,bookdb,token):
    response = client.patch(
        f"books/{bookdb.id}",json={
            "year": 1999,
            "title": "testetesteteste",
            "novelist_id": 34
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "year": 1999,
        "title": "testetesteteste",
        "novelist_id": 34
    }


def test_patch_book_year(client,bookdb,token):
    response = client.patch(
        f"books/{bookdb.id}",json={
            "year": 1971
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "year": 1971,
        "title": "book test",
        "novelist_id": 2
    }


def test_patch_book_error_not_found(client,token,bookdb):
    response=client.patch(
        f"books/{bookdb.id + 1}",json={
            "year": 1999,
            "title": "testetesteteste",
            "novelist_id": 34
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"Book not listed in MADR"}


def test_patch_book_title_error(client,token,bookdb,bookdb2):
    response=client.patch(
        f"books/{bookdb.id}",json={
            "title":bookdb2.title
        },headers={"Authorization":f"bearer {token}"}
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail":"This title already exists!"}


def test_get_book_id(client,bookdb):
    response=client.get(
        f"books/{bookdb.id}"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id":1,
        "year": 1900,
        "title": "book test",
        "novelist_id": 2
    }


def test_get_book_id_not_found(client,bookdb):
    response=client.get(
        f"books/{bookdb.id + 1}"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail":"Book not listed in MADR"}


def test_get_books_no_filter(client):
    response=client.get(
        "books"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"books":[]}


def test_get_books_with_filter_title(client,bookdb,bookdb2):
    response=client.get(
        "books?title=boo"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "books":[
            {
                "id": 1,
                "year": 1900,
                "title": "book test",
                "novelist_id": 2
            },
            {
                "id": 2,
                "year": 1901,
                "title": "book test2",
                "novelist_id": 3
            }
        ]
    }


def test_get_books_with_filter_title_and_year(client,bookdb,bookdb2):
    response=client.get(
        "books?title=boo&year=1901"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "books":[
            {
                "id": 2,
                "year": 1901,
                "title": "book test2",
                "novelist_id": 3
            }
        ]
    }