# Oraclynt — Producto y backlog ágil

## Visión

Plataforma institucional para operar bases Oracle mediante capacidades
gobernadas, trazables y seguras. La voz y la IA serán interfaces futuras; no
sustituirán autorización, política ni control humano.

## Épicas

| ID | Épica | Prioridad | Estado |
|---|---|---|---|
| E1 | MVP read-only y auditoría | P0 | Implementada |
| E2 | Grilla paginada y filtros | P0 | Implementada |
| E3 | Connection Manager seguro | P0 | Backend inicial |
| E4 | Descubrimiento dinámico de metadata | P0 | Backend inicial |
| E5 | Editor de consultas gobernado | P1 | Pendiente |
| E6 | Voz/STT/TTS sobre capacidades | P1 | Pendiente |
| E7 | IA asistida con revisión humana | P1 | Pendiente |
| E8 | Escrituras con aprobación | P2 | Bloqueada |
| E9 | Observabilidad y operación empresarial | P1 | Pendiente |

## Historias prioritarias

### HU-E1-01 — Ejecutar consulta registrada

Como analista, quiero ejecutar una operación read-only registrada sin enviar
SQL arbitrario. Aceptación: `validate` no ejecuta; `execute` requiere
validación, RBAC, correlation_id y adapter.

### HU-E2-01 — Explorar datos

Como analista, quiero ver filas paginadas, filtrar por columna y ordenar
resultados. Aceptación: límite máximo, paginación sin solape, errores
fail-closed y auditoría.

### HU-E3-01 — Probar conexión

Como administrador autorizado, quiero probar host, puerto, servicio y usuario
sin guardar la contraseña en el perfil. Aceptación: proveedor seguro,
secretos ausentes de API/logs y resultado auditable.

### HU-E4-01 — Descubrir catálogo

Como usuario autorizado, quiero ver únicamente esquemas y objetos reales que
Oracle devuelve y sobre los que tengo permiso. Aceptación: árbol expandible,
catálogo dinámico y sin nombres hardcodeados.

### HU-E5-01 — Consulta gobernada

Como analista, quiero construir consultas desde plantillas y parámetros
permitidos con vista previa. Aceptación: binds, timeout, máximo de filas y
política validada.

## Fuera de alcance

Escrituras Oracle, DDL, SQL libre, IA autónoma, voz real, producción,
autenticación corporativa y cambios de esquema requieren una fase autorizada.
