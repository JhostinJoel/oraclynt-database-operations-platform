from fastapi.testclient import TestClient
from app.main import app
from app.catalog import TestMetadataAdapter

client = TestClient(app)

def test_connection_profile_never_contains_secret():
    response = client.post("/connections", json={"name":"ORCL","host":"127.0.0.1","port":1521,"service":"orcl","username":"COMERCIAL","credential_reference":"runtime-config"})
    assert response.status_code == 200
    body = response.json()
    assert "password" not in body and "secret" not in body
    assert body["mode"] == "READ_ONLY"

def test_catalog_test_adapter_is_empty_and_safe():
    assert TestMetadataAdapter().discover("default-orcl") == []

def test_catalog_rejects_unknown_connection_in_oracle_adapter(monkeypatch):
    monkeypatch.setattr("app.main.metadata_adapter", __import__("app.catalog", fromlist=["OracleMetadataAdapter"]).OracleMetadataAdapter())
    response = client.get("/connections/not-registered/catalog")
    assert response.status_code == 502
