from fastapi.testclient import TestClient
from app.main import app, connection_manager

client = TestClient(app)

def profile_payload():
    return {"name":"ORCL-TEST","host":"192.168.56.101","port":1521,"service":"orcl","username":"COMERCIAL","credential_reference":"runtime-config"}

def test_create_list_and_get_connection_without_secret():
    connection_manager.profiles.clear()
    created = client.post("/connections", json=profile_payload())
    assert created.status_code == 200
    body = created.json()
    assert body["id"] == "default-orcl"
    assert "password" not in body and "secret" not in body
    listed = client.get("/connections")
    assert listed.status_code == 200 and len(listed.json()) == 1
    fetched = client.get("/connections/default-orcl")
    assert fetched.status_code == 200 and fetched.json()["username"] == "COMERCIAL"

def test_unknown_connection_is_rejected():
    assert client.get("/connections/unknown/catalog").status_code in {200, 502}
    assert client.get("/connections/unknown").status_code == 404

def test_connection_contract_rejects_invalid_port():
    payload = profile_payload(); payload["port"] = 70000
    assert client.post("/connections", json=payload).status_code == 422

def test_connection_test_never_returns_password(monkeypatch):
    monkeypatch.setattr("app.main.connection_manager.test", lambda request: {"status":"connected", "connection_id":"default-orcl"})
    response = client.post("/connections/test", json=profile_payload())
    assert response.status_code == 200
    assert "password" not in response.text.lower()
