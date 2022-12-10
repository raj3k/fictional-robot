import pytest
from app import schemas


def test_get_posts(client, test_posts):
    response = client.get("/posts/")

    def validate(post):
        return schemas.PostResponse(**post)

    posts_list = [validate(post) for post in response.json()]

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authenticated_client, test_user, title, content, published):
    response = authenticated_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authenticated_client, test_user, test_posts):
    res = authenticated_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user):
    response = client.post("/posts/", json={"title": "title", "content": "content"})

    assert response.status_code == 401


def test_get_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostResponse(**response.json())
    assert response.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.published == test_posts[0].published


def test_get_post_not_found(client, test_posts):
    response = client.get(f"/posts/1000000000")
    assert response.status_code == 404


def test_delete_post_success(authenticated_client, test_posts):
    response = authenticated_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204


def test_delete_post_not_found(authenticated_client, test_posts):
    response = authenticated_client.delete("/posts/100000")

    assert response.status_code == 404


def test_delete_post_unauthenticated_user(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_delete_other_user_post(authenticated_client, test_posts):
    response = authenticated_client.delete(f"/posts/{test_posts[3].id}")

    assert response.status_code == 403


def test_update_post_success(authenticated_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authenticated_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data["title"]


def test_update_post_not_found(authenticated_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    response = authenticated_client.put("/posts/10000000", json=data)

    assert response.status_code == 404


def test_update_post_unauthenticated_user(client, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401


def test_update_other_user_post(authenticated_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id

    }
    res = authenticated_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403



