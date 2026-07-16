# SQL — punto de partida

[Inicio](../README.md) → Contrato SQL

Este directorio contiene únicamente el contrato de tablas madre.

```text
schema.sql        -> crea PK, FK, restricciones, catálogos y hechos base
drop_tables.sql   -> reset compatible con el esquema anterior
security_etl_user.sql -> permisos mínimos del ETL
```

No existen views mantenidas. Su diseño se documentará en la siguiente fase, después de validar datos, claves y granos.

Contrato de diseño: [`docs/02_marco_analisis_datos/view_design/README.md`](../docs/02_marco_analisis_datos/view_design/README.md).

Cuando una ficha sea aprobada, su SQL se incorporará modularmente:

```text
sql/views/descriptive/
sql/views/diagnostic/
sql/views/predictive/
sql/views/prescriptive/
```

Las carpetas se crearán al implementar la primera view de cada módulo; no contienen todavía SQL.

## Tablas de única verdad

La finalidad, claves, relaciones, actualización, uso y limitaciones de cada
tabla están centralizadas en el [diccionario de tablas madre](../docs/02_marco_analisis_datos/data_model.md#diccionario-de-tablas-madre).

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
