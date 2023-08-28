# coding: utf-8

from fastapi.testclient import TestClient
from openapi_server.models.user_score_dto import UserScoreDTO  # noqa: F401


def test_get_score_user_get_user_id(client: TestClient):
    """Test case for get_score_user_get_user_id

    User score
    """

    headers = {}
    response = client.request(
        "GET",
        "/score/user/{user_id}".format(user_id="user_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
