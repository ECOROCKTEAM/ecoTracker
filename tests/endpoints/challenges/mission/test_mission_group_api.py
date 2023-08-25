from fastapi.testclient import TestClient


def test_get_mission_comminuty_list(client: TestClient):
    """Test case for get_mission_comminuty_list

    Mission group list
    """
    mission_group_filter = {"group_id": 0, "group_id_list": [6, 6], "mission_id": 1, "status": "status"}
    params = [("order", "order_example"), ("pagination", "pagination_example")]
    headers = {}
    response = client.request(
        "GET",
        "/mission/groups/list",
        headers=headers,
        json=mission_group_filter,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_mission_group_get_id(client: TestClient):
    """Test case for get_mission_group_get_id

    Mission group
    """

    headers = {}
    response = client.request(
        "GET",
        "/mission/groups/get/{id}".format(id="id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_patch_mission_group_update_id(client: TestClient):
    """Test case for patch_mission_group_update_id

    Update mission group
    """
    mission_group_update_dto = {
        "people_max": 6,
        "date_close": "2000-01-23T04:56:07.000+00:00",
        "comment": "comment",
        "place": "place",
        "meeting_date": "2000-01-23T04:56:07.000+00:00",
        "people_required": 0,
        "status": "status",
    }

    headers = {}
    response = client.request(
        "PATCH",
        "/mission/groups/update/{id}".format(id="id_example"),
        headers=headers,
        json=mission_group_update_dto,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_mission_group_create(client: TestClient):
    """Test case for post_mission_group_create

    Mission group create
    """
    mission_group_create_dto = {
        "people_max": 1,
        "author": "author",
        "mission_id": 0,
        "comment": "comment",
        "place": "place",
        "meeting_date": "2000-01-23T04:56:07.000+00:00",
        "people_required": 6,
        "status": "status",
    }

    headers = {}
    response = client.request(
        "POST",
        "/mission/groups/create",
        headers=headers,
        json=mission_group_create_dto,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
