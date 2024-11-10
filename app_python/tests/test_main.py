from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_read_root_success():
    response = client.get("/")
    assert response.status_code == 200
    assert "hello there" in response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_read_root_template_context():
    response = client.get("/")
    assert "text" in response.context
    assert (
        response.context["text"]
        == 'hello there\n want to visit <a href="/time">time</a>'
    )


def test_read_time_success():
    response = client.get("/time")
    assert response.status_code == 200
    assert "Time" in response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_read_time_template_context():
    response = client.get("/time")
    assert "text" in response.context
    assert "title" in response.context
    assert response.context["title"] == "Time"
    # Verify time string format
    time_str = response.context["text"]
    assert len(time_str) == 19  # YYYY-MM-DD HH:MM:SS
    assert time_str[4] == "-" and time_str[7] == "-"  # Date separators
    assert time_str[13] == ":" and time_str[16] == ":"  # Time separators


def test_static_files():
    # Test static files endpoint exists
    response = client.get("/static/")
    assert response.status_code in [404, 403]  # Directory listing should be disabled


def test_invalid_endpoint():
    response = client.get("/nonexistent")
    assert response.status_code == 404
