import pytest

from app import schemas, config
from jose import jwt


def test_login(client, test_user):
    response = client.post("/auth/login", data={"username": test_user["email"], "password": test_user["password"]})

    login_response = schemas.Token(**response.json())

    payload = jwt.decode(login_response.access_token, config.settings.secret_key, algorithms=[config.settings.algorithm])

    user_id = payload.get("user_id")

    assert response.status_code == 200
    assert login_response.token_type == "bearer"
    assert test_user["id"] == user_id


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@example.com", "password123", 403),
    ("example@gmail.com", "wrongpassword", 403),
    ("wrongemail@example.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("example@gmail.com", None, 422)
])
def test_failed_login(client, email, password, status_code):
    response = client.post("/auth/login", data={"username": email, "password": password})

    assert response.status_code == status_code
