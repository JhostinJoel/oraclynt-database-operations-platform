# Oraclynt — Ciclo de vida y gobierno

## Flujo obligatorio

```text
Idea → requisito → HU → diseño → implementación → pruebas → seguridad
→ revisión → release candidate → autorización → despliegue → operación
→ métricas → retrospectiva
```

## Requisitos

Cada requisito debe tener ID estable, responsable, prioridad, fuente,
dependencias, riesgos, criterios de aceptación y evidencia esperada.

## Definition of Ready

Una historia entra al sprint solo con objetivo, actor, alcance, criterios
verificables, datos de prueba, riesgos y dependencias resueltas. Si requiere
Oracle, credenciales, LLM o infraestructura debe existir
`ARCHITECTURE_DECISION_REQUIRED`.

## Definition of Done

- Código revisado y cambio mínimo.
- Tests unitarios, integración y negativos relevantes.
- RBAC, política, auditoría y correlation_id verificados.
- Sin secretos, SQL libre ni cambios no autorizados.
- Tests, lint, tipos, seguridad y build pasan cuando estén configurados.
- Documentación, diff y trazabilidad actualizados.

## Catálogos controlados

Mantener versionados el Command Registry, roles/políticas, referencias de
credenciales, metadata descubierta, códigos de error, ambientes, decisiones,
riesgos y la matriz requisito → HU → prueba → release.

## Ramas y releases

`main` debe permanecer integrable. Los cambios se revisan antes de fusionar.
Los tags identifican estados reproducibles. No declarar producción sin gates
de seguridad, rendimiento, rollback y observabilidad.

## Calidad y cambios

Separar FACT, EVIDENCIA, INFERENCIA e HIPÓTESIS. Todo cambio debe declarar
motivo, impacto, riesgo, reversión y pruebas. Nunca ocultar fallos desactivando
tests o debilitando políticas.

## Gate de producción

Requiere aprobación explícita, threat model, credenciales gestionadas,
rollback probado, observabilidad, pruebas de carga y evidencia de ausencia de
escrituras no autorizadas. Hasta entonces: TEST/PAPER/SHADOW.
