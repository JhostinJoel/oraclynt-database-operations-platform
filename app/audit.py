from app.models import AuditEvent


class AuditStore:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> AuditEvent:
        self.events.append(event)
        return event

    def get(self, correlation_id: str) -> AuditEvent | None:
        return next((e for e in self.events if e.correlation_id == correlation_id), None)


audit_store = AuditStore()

