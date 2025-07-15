from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.fixture
def mock_send_prompt(monkeypatch):
    def fake_send_prompt(prompt, model):
        return {"choices": [{"message": {"content": f"Echo: {prompt}"}}]}
    monkeypatch.setattr("openrouter_client.send_prompt", fake_send_prompt)

def test_chat(mock_send_prompt):
    payload = {"prompt": "Hello!", "model": "mistral"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"].startswith("Echo: ")
    assert "latency" in data
    assert "prompt_tokens" in data
    assert "response_tokens" in data 