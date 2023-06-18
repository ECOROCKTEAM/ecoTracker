from fastapi.testclient import TestClient


def test_get_mission_user_get_id(client: TestClient):
    """Test case for get_mission_user_get_id

    Get user mission
    """

    headers = {}
    response = client.request(
        "GET",
        "/mission/user/get/{id}".format(id="id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_mission_user_list(client: TestClient):
    """Test case for get_mission_user_list

    User mission list
    """
    mission_user_filter = {"mission_id": 0, "status": "status"}
    params = [("order", "order_example"), ("pagination", "pagination_example")]
    headers = {}
    response = client.request(
        "GET",
        "/mission/user/list",
        headers=headers,
        json=mission_user_filter,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_patch_mission_user_update_id(client: TestClient):
    """Test case for patch_mission_user_update_id

    Update user mission
    """
    mission_user_update_dto = {"date_close": "2000-01-23T04:56:07.000+00:00", "status": "status"}

    headers = {}
    response = client.request(
        "PATCH",
        "/mission/user/update/{id}".format(id="id_example"),
        headers=headers,
        json=mission_user_update_dto,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_mission_user_create(client: TestClient):
    """Test case for post_mission_user_create

    Create user mission
    """
    mission_user_create_dto = {"mission_id": 0, "status": "status"}

    headers = {}
    response = client.request(
        "POST",
        "/mission/user/create",
        headers=headers,
        json=mission_user_create_dto,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
