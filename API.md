# API del MVP

- `GET /health`: comprueba que la aplicación está activa.
- `GET /ready`: comprueba disponibilidad; devuelve `503` con kill switch activo.
- `POST /commands/interpret`: convierte texto en intención; nunca ejecuta.
- `GET /commands/{command_id}`: consulta el contrato de un comando registrado.
- `POST /commands/validate`: valida esquema, registry y RBAC; nunca ejecuta.
- `POST /commands/execute`: ejecuta únicamente una intención validada.
- `GET /audit/events/{correlation_id}`: recupera el evento auditable.

Todas las fases conservan `correlation_id` y distinguen `INTERPRET`, `VALIDATE`
y `EXECUTE`.
