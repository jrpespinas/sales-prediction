from fastapi.testclient import TestClient

from app.router.index import router

client = TestClient(router)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}
