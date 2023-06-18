from fastapi.testclient import TestClient


def test_get_task_get_task_id(client: TestClient):
    """Test case for get_task_get_task_id

    Get task
    """

    headers = {}
    response = client.request(
        "GET",
        "/task/get/{task_id}".format(task_id="task_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_task_list(client: TestClient):
    """Test case for get_task_list

    Task list
    """
    params = [("category_id", 56)]
    headers = {}
    response = client.request(
        "GET",
        "/task/list/{pagination_obj}/{sorting_obj}".format(
            pagination_obj="pagination_obj_example", sorting_obj="sorting_obj_example"
        ),
        headers=headers,
        params=params,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
