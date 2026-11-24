from app import app


def test_metrics_endpoint_exposes_http_metrics():
    client = app.test_client()
    client.get("/health")

    response = client.get("/metrics")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "http_requests_total" in body
    assert 'route="/health"' in body
    assert "http_request_duration_seconds_bucket" in body


def test_unknown_route_uses_bounded_label():
    client = app.test_client()
    client.get("/does-not-exist-123")

    body = client.get("/metrics").get_data(as_text=True)

    assert "does-not-exist-123" not in body
    assert 'route="unknown"' in body


def test_error_endpoint_returns_200_or_500():
    client = app.test_client()
    assert client.get("/error").status_code in (200, 500)
