# Oracle Governed Assistant

MVP text-first, read-only y fail-closed. El LLM no ejecuta SQL ni autoriza operaciones. Esta primera implementación usa un registry y adapter en memoria para pruebas; no conecta a Oracle ni a producción.

## Ejecutar

```powershell
python -m pip install -e ".[dev]"
pytest
uvicorn app.main:app --reload
```

## Estado de seguridad

`READ_ONLY=true`, `PRODUCTION_WRITES=false`, `ARBITRARY_SQL=false` y `ARBITRARY_PLSQL=false` son obligatorios. La integración Oracle real, autenticación OIDC y STT/TTS son FUTURE_SCOPE hasta definir sus contratos y secretos.
# oraclynt-database-operations-platform

