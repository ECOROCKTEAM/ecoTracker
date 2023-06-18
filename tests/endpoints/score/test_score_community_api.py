from fastapi.testclient import TestClient


def test_get_score_get_community_community_id(client: TestClient):
    """Test case for get_score_get_community_community_id

    Community score
    """

    headers = {}
    response = client.request(
        "GET",
        "/score/get_community/{community_id}".format(community_id="community_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
