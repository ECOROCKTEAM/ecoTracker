from fastapi.testclient import TestClient


def test_get_mission_get_mission_id(client: TestClient):
    """Test case for get_mission_get_mission_id

    Get mission
    """

    headers = {}
    response = client.request(
        "GET",
        "/mission/get/{mission_id}".format(mission_id=3.4),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_mission_list(client: TestClient):
    """Test case for get_mission_list

    Mission list
    """
    params = [("active", True), ("pagination", None), ("order", None)]
    headers = {}
    response = client.request(
        "GET",
        "/mission/list",
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
