from abc import ABC, abstractmethod
from typing import Any
from app.models import Intent
from app.config import settings

class DataAdapter(ABC):
    @abstractmethod
    def execute(self, operation: str, intent: Intent, max_rows: int) -> list[dict[str, Any]]:
        raise NotImplementedError

class TestMemoryAdapter(DataAdapter):
    __test__ = False
    def __init__(self) -> None:
        self.calls: list[str] = []
    def execute(self, operation: str, intent: Intent, max_rows: int) -> list[dict[str, Any]]:
        self.calls.append(operation)
        if operation not in {"sales_by_country", "sales_detail"}:
            raise ValueError("UNKNOWN_ADAPTER_OPERATION")
        if operation == "sales_detail":
            rows = [{"id_venta": i, "pais": "PERU", "monto": 100 + i, "detalle": "Ventas Masiva"} for i in range(1, 1001)]
            if intent.pais:
                rows = [row for row in rows if row["pais"] == intent.pais]
            rows.sort(key=lambda row: row[intent.sort_column], reverse=intent.sort_direction == "DESC")
            return rows[intent.offset_rows:intent.offset_rows + max_rows]
        rows = [{"pais": "PERU", "total_rows": 1990000}, {"pais": "ZUISA", "total_rows": 10000}]
        if intent.pais:
            rows = [row for row in rows if row["pais"] == intent.pais]
        return rows[:max_rows]

test_adapter = TestMemoryAdapter()

class OracleDataAdapter(DataAdapter):
    def execute(self, operation: str, intent: Intent, max_rows: int) -> list[dict[str, Any]]:
        if operation not in {"sales_by_country", "sales_detail"}:
            raise ValueError("UNKNOWN_ADAPTER_OPERATION")
        if not all((settings.oracle_host, settings.oracle_service, settings.oracle_user, settings.oracle_password)):
            raise RuntimeError("ORACLE_CONFIGURATION_INCOMPLETE")
        try:
            import oracledb
        except ImportError as exc:
            raise RuntimeError("ORACLE_DRIVER_UNAVAILABLE") from exc
        if operation == "sales_detail":
            sort_column = {"id_venta": "ID_VENTA", "pais": "PAIS", "monto": "MONTO", "detalle": "DETALLE"}[intent.sort_column]
            sql = ("SELECT id_venta, pais, monto, detalle FROM comercial.ventas_lab "
                   "WHERE (:pais IS NULL OR pais = :pais) "
                   f"ORDER BY {sort_column} {intent.sort_direction} OFFSET :offset_rows ROWS FETCH NEXT :limit_rows ROWS ONLY")
        else:
            sql = ("SELECT pais, COUNT(*) AS total_rows, SUM(monto) AS total_monto FROM "
                   "comercial.ventas_lab WHERE (:pais IS NULL OR pais = :pais) GROUP BY pais ORDER BY pais")
        connection = cursor = None
        try:
            connection = oracledb.connect(user=settings.oracle_user, password=settings.oracle_password, host=settings.oracle_host, port=settings.oracle_port, service_name=settings.oracle_service)
            cursor = connection.cursor(); cursor.arraysize = min(max_rows, 1000)
            binds = {"pais": intent.pais}
            if operation == "sales_detail": binds.update(offset_rows=intent.offset_rows, limit_rows=min(max_rows, 500))
            cursor.execute(sql, binds)
            columns = [description[0].lower() for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchmany(max_rows)]
        except Exception as exc:
            raise RuntimeError("ORACLE_READ_ONLY_OPERATION_FAILED") from exc
        finally:
            if cursor is not None: cursor.close()
            if connection is not None: connection.close()
