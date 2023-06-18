from fastapi.testclient import TestClient


def test_get_task_user_get_task_id(client: TestClient):
    """Test case for get_task_user_get_task_id

    Get user task
    """

    headers = {}
    response = client.request(
        "GET",
        "/task/user/get/{task_id}".format(task_id="task_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_task_user_list(client: TestClient):
    """Test case for get_task_user_list

    List user tasks
    """

    headers = {}
    response = client.request(
        "GET",
        "/task/user/list/{pagination_obj}/{sorting_obj}".format(
            pagination_obj="pagination_obj_example", sorting_obj="sorting_obj_example"
        ),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_task_user_plan_list(client: TestClient):
    """Test case for get_task_user_plan_list

    Your GET endpoint
    """

    headers = {}
    response = client.request(
        "GET",
        "/task/user/plan/list",
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_task_user_add_task_id(client: TestClient):
    """Test case for post_task_user_add_task_id

    Add task to user list
    """

    headers = {}
    response = client.request(
        "POST",
        "/task/user/add/{task_id}".format(task_id=56),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_task_user_complete_task_id(client: TestClient):
    """Test case for post_task_user_complete_task_id

    Complete user task
    """

    headers = {}
    response = client.request(
        "POST",
        "/task/user/complete/{task_id}".format(task_id="task_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_post_task_user_reject_task_id(client: TestClient):
    """Test case for post_task_user_reject_task_id

    Reject User Task
    """

    headers = {}
    response = client.request(
        "POST",
        "/task/user/reject/{task_id}".format(task_id="task_id_example"),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
