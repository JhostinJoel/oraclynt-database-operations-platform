from abc import ABC, abstractmethod
from typing import Any
from app.config import settings
from app.models import CatalogNode

class MetadataAdapter(ABC):
    @abstractmethod
    def discover(self, connection_id: str, schema_name: str | None = None) -> list[CatalogNode]: ...

class TestMetadataAdapter(MetadataAdapter):
    def discover(self, connection_id: str, schema_name: str | None = None) -> list[CatalogNode]:
        return []

class OracleMetadataAdapter(MetadataAdapter):
    def discover(self, connection_id: str, schema_name: str | None = None) -> list[CatalogNode]:
        if connection_id != "default-orcl" or not settings.oracle_password:
            raise RuntimeError("METADATA_CONNECTION_UNAVAILABLE")
        conn = cur = None
        try:
            import oracledb
            conn = oracledb.connect(user=settings.oracle_user, password=settings.oracle_password, host=settings.oracle_host, port=settings.oracle_port, service_name=settings.oracle_service)
            cur = conn.cursor()
            if schema_name:
                cur.execute("SELECT object_name, object_type FROM all_objects WHERE owner = :owner AND object_type IN ('TABLE','VIEW','SEQUENCE','PROCEDURE','FUNCTION','PACKAGE','TRIGGER') ORDER BY object_type, object_name", {"owner": schema_name.upper()})
                rows = cur.fetchall()
                return [CatalogNode(name=name, node_type=kind, schema_name=schema_name.upper(), has_children=kind in {"TABLE", "VIEW"}) for name, kind in rows]
            cur.execute("SELECT username FROM all_users WHERE username = :owner ORDER BY username", {"owner": settings.oracle_user.upper()})
            return [CatalogNode(name=name, node_type="SCHEMA", has_children=True) for (name,) in cur.fetchall()]
        except Exception as exc:
            raise RuntimeError("ORACLE_METADATA_READ_FAILED") from exc
        finally:
            if cur is not None: cur.close()
            if conn is not None: conn.close()

metadata_adapter = OracleMetadataAdapter() if settings.app_env.upper() == "ORACLE" else TestMetadataAdapter()
