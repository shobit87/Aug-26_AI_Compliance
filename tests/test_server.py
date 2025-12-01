"""Basic FastAPI integration tests for the upload UI."""

from fastapi.testclient import TestClient

from ai_compliance_agent.server import app


def test_landing_page_renders():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Compliance Agent" in response.text


def test_upload_endpoint_returns_results():
    client = TestClient(app)
    files = {"document": ("policy.txt", b"Brief change policy summary", "text/plain")}
    response = client.post(
        "/analyze",
        data={"request_text": "Review SOC2 change policy"},
        files=files,
    )
    assert response.status_code == 200
    assert "Results" in response.text
    assert "Document Recommendations" in response.text
