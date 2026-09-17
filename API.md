# API

- `GET /health`: liveness.
- `GET /ready`: readiness; falla con kill switch activo.
- `POST /commands/validate`: valida command y roles sin ejecutar.
- `POST /commands/execute`: ejecuta solo comandos read-only registrados.
- `GET /audit/events/{correlation_id}`: recupera evidencia de la operación.

