from datetime import datetime, timezone
from uuid import uuid4
from app.config import settings
from app.models import ConnectionCreateRequest, ConnectionProfile, ConnectionTestRequest

class SecureCredentialProvider:
    def get_password(self, connection_id: str) -> str:
        if connection_id != "default-orcl" or not settings.oracle_password:
            raise RuntimeError("CREDENTIAL_UNAVAILABLE")
        return settings.oracle_password

class ConnectionManager:
    def __init__(self) -> None:
        self.profiles: dict[str, ConnectionProfile] = {}
        self.credentials = SecureCredentialProvider()

    def _profile(self, request: ConnectionTestRequest, credential_reference: str, environment: str = "TEST") -> ConnectionProfile:
        now = datetime.now(timezone.utc).isoformat()
        return ConnectionProfile(id="default-orcl", name=request.name, host=request.host, port=request.port, service=request.service, username=request.username, environment=environment, credential_reference=credential_reference, created_at=now, updated_at=now)

    def test(self, request: ConnectionTestRequest) -> dict[str, str]:
        profile = self._profile(request, "runtime-config")
        if profile.host == settings.oracle_host and profile.service == settings.oracle_service and settings.oracle_password:
            try:
                self.credentials.get_password(profile.id)
                import oracledb
                conn = oracledb.connect(user=profile.username, password=settings.oracle_password, host=profile.host, port=profile.port, service_name=profile.service)
                conn.close()
                return {"status": "connected", "connection_id": profile.id}
            except Exception as exc:
                raise RuntimeError("CONNECTION_TEST_FAILED") from exc
        return {"status": "not_tested", "connection_id": profile.id}

    def create(self, request: ConnectionCreateRequest) -> ConnectionProfile:
        profile = self._profile(request, request.credential_reference, request.environment)
        self.profiles[profile.id] = profile
        return profile

    def list(self) -> list[ConnectionProfile]:
        return list(self.profiles.values())

connection_manager = ConnectionManager()
