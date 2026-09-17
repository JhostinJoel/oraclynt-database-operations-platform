from dataclasses import dataclass
from typing import Any
from app.adapters import DataAdapter
from app.models import Intent


@dataclass(frozen=True)
class Command:
    command_id: str
    version: str
    allowed_roles: frozenset[str]
    operation: str
    max_rows: int = 1000


COMMANDS = {
    "consultar_ventas_por_pais": Command("consultar_ventas_por_pais", "v1", frozenset({"analyst", "admin"}), "sales_by_country"),
    "consultar_detalle_ventas": Command("consultar_detalle_ventas", "v1", frozenset({"analyst", "admin"}), "sales_detail", 500),
}


def get_command(action: str) -> Command | None:
    return COMMANDS.get(action)

def execute_command(command: Command, intent: Intent, adapter: DataAdapter, max_rows: int) -> list[dict[str, Any]]:
    return adapter.execute(command.operation, intent, min(command.max_rows, max_rows))
