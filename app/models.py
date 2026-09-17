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
