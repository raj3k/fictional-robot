from app import schemas


def test_create_user(client):
    response = client.post("/users/", json={"email": "email@example.com", "password": "password123"})

    new_user = schemas.UserResponse(**response.json())
    assert response.status_code == 201
    assert new_user.email == "email@example.com"


def test_get_user(client, test_user):
    response = client.get("/users/1")

    user = schemas.UserResponse(**response.json())

    assert response.status_code == 200
    assert user.email == "example@gmail.com"
