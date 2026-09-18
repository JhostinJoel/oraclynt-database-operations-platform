from typing import Any, Literal, Union
from pydantic import BaseModel, ConfigDict, Field


class Intent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: str
    period: Literal["hoy", "mes_actual", "mes_anterior"] | None = None
    group_by: Literal["pais"] | None = None
    pais: str | None = Field(default=None, max_length=50)
    region: str | None = Field(default=None, max_length=100)

class InterpretRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    user_id: str = Field(min_length=1, max_length=128)

class DetailIntent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    action: Literal["consultar_detalle_ventas"]
    pais: str | None = Field(default=None, max_length=50)
    offset_rows: int = Field(default=0, ge=0)
    limit_rows: int = Field(default=100, ge=1, le=500)
    sort_column: Literal["id_venta", "pais", "monto", "detalle"] = "id_venta"
    sort_direction: Literal["ASC", "DESC"] = "ASC"

class ValidationRequest(BaseModel):
    correlation_id: str
    user_id: str = Field(min_length=1, max_length=128)
    roles: list[str] = Field(default_factory=list)
    intent: Union[Intent, DetailIntent]

class ExecuteRequest(ValidationRequest):
    validation_id: str = Field(min_length=1)

class CommandRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    roles: list[str] = Field(default_factory=list)
    intent: Intent


class AuditEvent(BaseModel):
    correlation_id: str
    user_id: str
    roles: list[str]
    intent: dict[str, Any]
    command_id: str | None = None
    authorization_result: str
    execution_result: str
    row_count: int = 0
    error_code: str | None = None
    phase: Literal["INTERPRET", "VALIDATE", "EXECUTE"]
    transcript: str | None = None

class ConnectionTestRequest(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    host: str = Field(min_length=1, max_length=253)
    port: int = Field(default=1521, ge=1, le=65535)
    service: str = Field(min_length=1, max_length=128)
    username: str = Field(min_length=1, max_length=128)

class ConnectionProfile(BaseModel):
    id: str
    name: str
    host: str
    port: int
    service: str
    username: str
    environment: str = "TEST"
    mode: str = "READ_ONLY"
    credential_reference: str
    created_at: str
    updated_at: str

class ConnectionCreateRequest(ConnectionTestRequest):
    environment: str = "TEST"
    mode: Literal["READ_ONLY"] = "READ_ONLY"
    credential_reference: str = Field(min_length=1, max_length=128)

class CatalogNode(BaseModel):
    name: str
    node_type: str
    schema_name: str | None = None
    has_children: bool = False

class CatalogResponse(BaseModel):
    connection_id: str
    correlation_id: str
    nodes: list[CatalogNode]
