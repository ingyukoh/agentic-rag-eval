from fastapi.testclient import TestClient

from agentic_rag_eval.api import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_query_contract() -> None:
    response = client.post("/query", json={"query": "Report MSFT net income for fiscal 2024."})
    assert response.status_code == 200
    body = response.json()
    assert body["answerable"] is True
    assert body["value"] == 88_136_000_000
    assert body["citation_id"] == "msft-2024-net-income"
