import re
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.adapters import OracleDataAdapter, test_adapter
from app.audit import audit_store
from app.config import settings
from app.models import AuditEvent, ExecuteRequest, InterpretRequest, ValidationRequest
from app.registry import execute_command, get_command

app = FastAPI(title="Oracle Governed Assistant", version="0.1.0")
data_adapter = OracleDataAdapter() if settings.app_env.upper() == "ORACLE" else test_adapter
validations: dict[str, tuple[str, str, list[str], object]] = {}

def add_audit(**kwargs: object) -> None:
    audit_store.append(AuditEvent(**kwargs))

def reject_text(text: str) -> bool:
    return bool(re.search(
        r"\b(drop|delete|update|insert|alter|truncate|grant|revoke|create)\b"
        r"|pl[/ ]?sql|\bexec(?:ute)?\b"
        r"|ignore\s+(?:the|all)\s+rules|ignora\s+(?:las|todas\s+las)\s+reglas"
        r"|consulta\s+cualquier\s+tabla|any\s+table",
        text, re.I,
    ))

@app.get("/health")
def health() -> dict[str, str]: return {"status": "ok"}

@app.get("/ready")
def ready() -> dict[str, str]:
    if settings.kill_switch: raise HTTPException(503, "KILL_SWITCH_ACTIVE")
    return {"status": "ready"}

@app.post("/commands/interpret")
def interpret(request: InterpretRequest) -> dict[str, object]:
    correlation_id = str(uuid4())
    if reject_text(request.text):
        add_audit(correlation_id=correlation_id, user_id=request.user_id, roles=[], intent={}, authorization_result="NOT_APPLICABLE", execution_result="REJECTED", error_code="MALICIOUS_INPUT", phase="INTERPRET", transcript=request.text)
        raise HTTPException(400, "REJECTED")
    text = request.text.lower()
    intent = {"action": "consultar_ventas_por_pais", "period": None, "group_by": "pais", "pais": None}
    add_audit(correlation_id=correlation_id, user_id=request.user_id, roles=[], intent=intent, authorization_result="NOT_APPLICABLE", execution_result="NOT_EXECUTED", phase="INTERPRET", transcript=request.text)
    return {"correlation_id": correlation_id, "intent": intent}

@app.get("/commands/{command_id}")
def command_info(command_id: str) -> dict[str, object]:
    command = get_command(command_id)
    if command is None: raise HTTPException(404, "COMMAND_NOT_FOUND")
    return {"command_id": command.command_id, "version": command.version, "allowed_roles": sorted(command.allowed_roles), "operation": command.operation, "max_rows": command.max_rows}

@app.post("/commands/validate")
def validate(request: ValidationRequest) -> dict[str, object]:
    if settings.kill_switch: raise HTTPException(503, "KILL_SWITCH_ACTIVE")
    command = get_command(request.intent.action)
    if command is None or not command.allowed_roles.intersection(request.roles): raise HTTPException(403 if command else 400, "REJECTED")
    validation_id = str(uuid4())
    validations[validation_id] = (request.correlation_id, request.user_id, request.roles, request.intent)
    add_audit(correlation_id=request.correlation_id, user_id=request.user_id, roles=request.roles, intent=request.intent.model_dump(), command_id=command.command_id, authorization_result="AUTHORIZED", execution_result="NOT_EXECUTED", phase="VALIDATE")
    return {"correlation_id": request.correlation_id, "validation_id": validation_id, "status": "validated"}

@app.post("/commands/execute")
def execute(request: ExecuteRequest) -> dict[str, object]:
    record = validations.get(request.validation_id)
    if record is None or record[:3] != (request.correlation_id, request.user_id, request.roles) or record[3] != request.intent: raise HTTPException(403, "REJECTED")
    if settings.kill_switch or not settings.read_only or settings.production_writes or settings.arbitrary_sql or settings.arbitrary_plsql: raise HTTPException(503, "SECURITY_REJECTION")
    command = get_command(request.intent.action)
    if command is None: raise HTTPException(400, "REJECTED")
    rows = execute_command(command, request.intent, data_adapter, settings.max_rows)
    add_audit(correlation_id=request.correlation_id, user_id=request.user_id, roles=request.roles, intent=request.intent.model_dump(), command_id=command.command_id, authorization_result="AUTHORIZED", execution_result="SUCCESS", row_count=len(rows), phase="EXECUTE")
    return {"correlation_id": request.correlation_id, "command_id": command.command_id, "rows": rows}

@app.get("/audit/events/{correlation_id}", response_model=AuditEvent)
def get_audit(correlation_id: str) -> AuditEvent:
    event = audit_store.get(correlation_id)
    if event is None: raise HTTPException(404, "AUDIT_EVENT_NOT_FOUND")
    return event

app.mount("/", StaticFiles(directory="static", html=True), name="frontend")
