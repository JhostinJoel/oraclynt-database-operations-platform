# Arquitectura de conexiones y metadata

El bloque inicial separa tres responsabilidades:

```text
API → ConnectionManager → SecureCredentialProvider
API → MetadataAdapter → Oracle metadata
```

Los perfiles contienen host, puerto, service, usuario, ambiente y una
referencia de credencial, nunca la contraseña. En TEST el adapter de metadata
devuelve un catálogo vacío: no inventa objetos. En ORACLE consulta únicamente
metadata visible mediante vistas `ALL_*`, usando binds para valores.

El catálogo se solicita por conexión y opcionalmente por esquema, lo que
permite lazy loading. La siguiente iteración debe completar permisos por nodo,
detalle de columnas, índices y constraints, y conectar el árbol del frontend
a esta API. La grilla sigue usando operaciones read-only gobernadas.
