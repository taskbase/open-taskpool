from fastapi.testclient import TestClient
from . import client, app


def test_healthcheck(client: TestClient):
    response = client.get("/healthcheck")
    assert response.status_code == 200

    response_json = response.json()
    assert response_json["healthy"]
    assert response_json["status"] == "Up and running!"
