from fastapi.testclient import TestClient


def test_get_score_get_group_group_id(client: TestClient):
    """Test case for get_score_get_group_group_id

    group score
    """

    headers = {}
    response = client.request(
        "GET",
        "/score/groups/{group_id}".format(group_id="group_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
