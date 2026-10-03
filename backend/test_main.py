from fastapi.testclient import TestClient
from main import app


def test_health():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}


def test_crud():
    with TestClient(app) as client:
        created = client.post("/todos", json={"title": "test"}).json()
        todo_id = created["id"]

        assert client.get(f"/todos/{todo_id}").json()["title"] == "test"

        r = client.put(f"/todos/{todo_id}", json={"title": "test", "done": True})
        assert r.json()["done"] is True

        assert client.delete(f"/todos/{todo_id}").status_code == 200
        assert client.get(f"/todos/{todo_id}").status_code == 404