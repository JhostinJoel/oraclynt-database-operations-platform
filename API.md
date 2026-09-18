# API del MVP

- `GET /health`: comprueba que la aplicación está activa.
- `GET /ready`: comprueba disponibilidad; devuelve `503` con kill switch activo.
- `POST /commands/interpret`: convierte texto en intención; nunca ejecuta.
- `GET /commands/{command_id}`: consulta el contrato de un comando registrado.
- `POST /commands/validate`: valida esquema, registry y RBAC; nunca ejecuta.
- `POST /commands/execute`: ejecuta únicamente una intención validada.
- `GET /audit/events/{correlation_id}`: recupera el evento auditable.
- `POST /connections/test`: prueba una conexión sin devolver credenciales.
- `POST /connections`: registra un perfil sin almacenar la contraseña.
- `GET /connections`: lista perfiles sanitizados.
- `GET /connections/{id}/catalog`: descubre metadata visible de forma read-only.

Todas las fases conservan `correlation_id` y distinguen `INTERPRET`, `VALIDATE`
y `EXECUTE`.
