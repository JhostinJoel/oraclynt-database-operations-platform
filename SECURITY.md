# Línea base de seguridad

El sistema rechaza comandos fuera del registry, valida la intención con
Pydantic, aplica RBAC antes de ejecutar y registra auditoría con
`correlation_id`. No acepta SQL, PL/SQL, nombres de tablas ni columnas
arbitrarias.

La configuración insegura activa rechazo global. Deben mantenerse:

```text
READ_ONLY=true
PRODUCTION_WRITES=false
ARBITRARY_SQL=false
ARBITRARY_PLSQL=false
```

Las credenciales Oracle solo pueden residir en configuración local segura. No
se devuelven por API ni se escriben en logs.
