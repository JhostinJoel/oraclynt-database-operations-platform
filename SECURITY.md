# Security baseline

El sistema rechaza comandos fuera del registry, valida el intent con Pydantic, aplica roles antes de ejecutar y registra un evento de auditoría con `correlation_id`. No acepta SQL, PL/SQL, nombres de tablas ni columnas arbitrarias. La configuración insegura activa rechazo global.

