from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# CREATE


def test_create_task_success():
    response = client.post(
        "/tasks/", json={"title": "Test", "description": ""}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
    assert response.json()["description"] == ""


def test_create_task_without_title():
    response = client.post("/tasks/", json={"description": ""})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


def test_create_task_with_empty_title():
    response = client.post("/tasks/", json={"title": "", "description": ""})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


def test_create_task_with_101_symbols():
    long_title = "A" * 101
    response = client.post(
        "/tasks/", json={"title": long_title, "description": ""}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "title"]


def test_create_task_without_description():
    response = client.post("/tasks/", json={"title": "Test"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
    assert response.json()["description"] is None


# READ


def test_get_correct_task():
    create_response = client.post("/tasks/", json={"title": "Test"})
    task_id = create_response.json()["id"]
    response = client.get(f"/task/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test"
    assert response.json()["description"] is None


def test_get_nonexist_id():
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_get_invalid_id():
    response = client.get("/tasks/abc")
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "int_parsing"


# Read ALL


def test_get_all_tasks_empty():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_tasks_one_task():
    client.post("/tasks/", json={"title": "Test"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test"


def test_get_all_tasks_multiple():
    client.post("/tasks/", json={"title": "Test1"})
    client.post("/tasks/", json={"title": "Test2"})
    client.post("/tasks/", json={"title": "Test3"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    titles = [task["title"] for task in data]
    assert "Test1" in titles
    assert "Test2" in titles
    assert "Test3" in titles


# Update
def test_update_task_all_fields():
    create_response = client.post("/tasks/", json={"title": "Test"})
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Test1", "description": "Test", "status": "done"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test1"
    assert data["description"] == "Test"
    assert data["status"] == "done"


def test_update_task_title_only():
    create_response = client.post(
        "/tasks/", json={"title": "Test", "description": ""}
    )
    task_id = create_response.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": "Test1"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test1"
    assert data["description"] == ""
    assert data["status"] == "todo"


def test_update_task_status_only():
    create_response = client.post(
        "/tasks/", json={"title": "Test", "description": ""}
    )
    task_id = create_response.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}", json={"status": "in_progress"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["description"] == ""
    assert data["status"] == "in_progress"


def test_update_nonexistent_task():
    response = client.patch("/tasks/9999", json={"title": "Test"})
    assert response.status_code == 404


def test_update_task_invalid_status():
    create_response = client.post("/tasks/", json={"title": "Test"})
    task_id = create_response.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "cancelled"})
    assert response.status_code == 422


def test_update_task_empty_body():
    create_response = client.post(
        "/tasks/", json={"title": "Test", "description": "Description"}
    )
    task_id = create_response.json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["description"] == "Description"
    assert data["status"] == "todo"


def test_delete_task():
    create_response = client.post(
        "/tasks/", json={"title": "Test", "description": ""}
    )
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204


def test_repeat_delete_task():
    create_response = client.post(
        "/tasks/", json={"title": "Test", "description": ""}
    )
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_delete_nonexistent_task():
    create_response = client.post(
        "/tasks/", json={"title": "Test", "description": ""}
    )
    task_id = create_response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404
