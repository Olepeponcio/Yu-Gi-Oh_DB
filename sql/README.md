# SQL — punto de partida

Este directorio contiene únicamente el contrato de tablas madre.

```text
schema.sql        -> crea PK, FK, restricciones, catálogos y hechos base
drop_tables.sql   -> reset compatible con el esquema anterior
security_etl_user.sql -> permisos mínimos del ETL
queries/          -> consultas exploratorias históricas; no forman el modelo semántico
```

No existen views mantenidas. Su diseño se documentará en la siguiente fase, después de validar datos, claves y granos.

## Tablas de única verdad

| Tabla | Grano |
|---|---|
| `cards` | una carta |
| `sets` | un set |
| `rarity_types` | una rareza semántica + código |
| `card_printings` | carta + código de impresión + rareza raw + código raw |
| `marketplaces` | un marketplace |
| `currencies` | una moneda |
| `card_price_history` | carta + marketplace + moneda + snapshot |

`card_price_history` es largo, append-only y sirve tanto para precio vigente —último snapshot— como para histórico. La rareza solo filtra precios de impresión (`set_price_usd`); no se atribuye a precios generales de carta.
