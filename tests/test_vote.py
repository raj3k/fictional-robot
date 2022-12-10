

def test_vote_on_post(authenticated_client, test_posts):
    response = authenticated_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "dir": 1})

    assert response.status_code == 201
    assert response.json()["message"] == "successfully added vote"


def test_vote_twice(authenticated_client, test_posts, test_vote):
    response = authenticated_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "dir": 1})

    assert response.status_code == 409


def test_vote_remove(authenticated_client, test_posts, test_vote):
    response = authenticated_client.post(
        "/votes/", json={"post_id": test_posts[3].id, "dir": 0})

    assert response.status_code == 200


def test_vote_not_exist(authenticated_client, test_posts):
    response = authenticated_client.post(
        "/votes/", json={"post_id": 100000, "dir": 0})

    assert response.status_code == 404


def test_vote_unauthenticated(client, test_posts):
    response = client.post(
        "/votes/", json={"post_id": test_posts[3].id, "dir": 1})

    assert response.status_code == 401

