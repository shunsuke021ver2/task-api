from fastapi.testclient import TestClient


def test_list_is_empty_initially(client: TestClient) -> None:
    res = client.get("/tasks")
    assert res.status_code == 200
    assert res.json() == []


def test_create_task_with_defaults(client: TestClient) -> None:
    res = client.post("/tasks", json={"title": "牛乳を買う"})
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "牛乳を買う"
    assert body["description"] == ""
    assert body["done"] is False
    assert body["id"]
    assert body["created_at"]


def test_create_task_rejects_empty_title(client: TestClient) -> None:
    res = client.post("/tasks", json={"title": ""})
    assert res.status_code == 422


def test_list_returns_created_tasks(client: TestClient) -> None:
    client.post("/tasks", json={"title": "a"})
    client.post("/tasks", json={"title": "b"})
    res = client.get("/tasks")
    assert [t["title"] for t in res.json()] == ["a", "b"]


def test_update_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "old"}).json()
    res = client.put(f"/tasks/{created['id']}", json={"title": "new", "done": True})
    assert res.status_code == 200
    body = res.json()
    assert body["id"] == created["id"]
    assert body["title"] == "new"
    assert body["done"] is True
    assert body["created_at"] == created["created_at"]


def test_update_task_partial(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "keep", "description": "d"}).json()
    res = client.put(f"/tasks/{created['id']}", json={"done": True})
    body = res.json()
    assert body["title"] == "keep"
    assert body["description"] == "d"
    assert body["done"] is True


def test_update_missing_task_returns_404(client: TestClient) -> None:
    res = client.put("/tasks/not-exist", json={"title": "x"})
    assert res.status_code == 404


def test_delete_task(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "temp"}).json()
    res = client.delete(f"/tasks/{created['id']}")
    assert res.status_code == 204
    assert client.get("/tasks").json() == []


def test_delete_missing_task_returns_404(client: TestClient) -> None:
    res = client.delete("/tasks/not-exist")
    assert res.status_code == 404
