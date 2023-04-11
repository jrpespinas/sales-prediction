from fastapi.testclient import TestClient

from ..routers.health_check import router

client = TestClient(router)


def test_index():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
