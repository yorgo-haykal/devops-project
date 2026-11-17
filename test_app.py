from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 201
    assert response.data == b"OK"