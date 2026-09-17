# Oraclynt Database Operations Platform

MVP text-first para consultar datos Oracle de forma gobernada, trazable y
read-only. El sistema no ejecuta SQL o PL/SQL arbitrario y permanece fail-closed.

## Inicio rápido

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8080
```

Abrir `http://127.0.0.1:8080`.

## Flujo seguro

```text
texto → intención → validación → autorización → registry → adapter → auditoría
```

`interpret` solo interpreta; `validate` valida y autoriza; `execute` requiere
una validación previa y ejecuta únicamente una operación registrada.

## Grilla de datos

La vista Datos muestra filas paginadas con sus columnas. Incluye filtros por
ID, país, monto y detalle, limpieza de filtros y ordenamiento por encabezado.
Los filtros actúan sobre la página cargada; la consulta continúa limitada por
la política read-only y por el máximo de filas configurado.

## Configuración segura

Copiar `.env.example` a `.env` y completar secretos solo localmente. Nunca
versionar `.env`, contraseñas, tokens ni credenciales.

Valores obligatorios:

```text
READ_ONLY=true
PRODUCTION_WRITES=false
ARBITRARY_SQL=false
ARBITRARY_PLSQL=false
```

## Estado y límites

El MVP actual cubre consultas registradas, adapter de pruebas, adapter Oracle
read-only, RBAC, kill switch, auditoría y pruebas automatizadas. El explorador
dinámico de todos los objetos de la instancia, voz, LLM productivo, STT/TTS,
CRUD y producción permanecen pendientes de una fase posterior.
# oraclynt-database-operations-platform

## Gobierno del desarrollo

- [Backlog y producto](docs/PRODUCT_BACKLOG_ES.md)
- [Ciclo de vida y gobierno](docs/SDLC_GOVERNANCE_ES.md)
