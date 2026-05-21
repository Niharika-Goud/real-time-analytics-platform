from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analytics():

    response = client.get(
        "/analytics/stats"
    )

    assert response.status_code == 200