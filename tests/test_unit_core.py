import pytest
from pydantic import ValidationError
from app.adapters import TestMemoryAdapter
from app.audit import AuditStore
from app.models import Intent
from app.registry import COMMANDS, execute_command, get_command


def test_intent_rejects_unknown_fields_and_invalid_group():
    with pytest.raises(ValidationError):
        Intent(action="consultar_ventas_por_pais", sql="DROP TABLE ventas")
    with pytest.raises(ValidationError):
        Intent(action="consultar_ventas_por_pais", group_by="region")


def test_registry_is_allowlist_and_has_no_sql():
    command = get_command("consultar_ventas_por_pais")
    assert command is not None
    assert set(COMMANDS) == {"consultar_ventas_por_pais", "consultar_detalle_ventas"}
    assert not hasattr(command, "sql")
    assert command.operation == "sales_by_country"


def test_adapter_filters_and_limits_results():
    adapter = TestMemoryAdapter()
    intent = Intent(action="consultar_ventas_por_pais", group_by="pais", pais="PERU")
    rows = adapter.execute("sales_by_country", intent, 1)
    assert len(rows) == 1
    assert rows[0]["pais"] == "PERU"
    assert adapter.calls == ["sales_by_country"]


def test_adapter_rejects_unknown_operation():
    with pytest.raises(ValueError, match="UNKNOWN_ADAPTER_OPERATION"):
        TestMemoryAdapter().execute("arbitrary_sql", Intent(action="x"), 10)


def test_registry_dispatches_only_through_adapter():
    adapter = TestMemoryAdapter()
    command = get_command("consultar_ventas_por_pais")
    rows = execute_command(command, Intent(action=command.command_id, group_by="pais"), adapter, 1)
    assert rows and adapter.calls == ["sales_by_country"]


def test_audit_store_returns_latest_event_without_secrets():
    store = AuditStore()
    from app.models import AuditEvent
    event = AuditEvent(correlation_id="c1", user_id="u1", roles=["analyst"], intent={}, authorization_result="AUTHORIZED", execution_result="SUCCESS", phase="EXECUTE")
    store.append(event)
    assert store.get("c1") == event
    assert "password" not in event.model_dump_json().lower()
