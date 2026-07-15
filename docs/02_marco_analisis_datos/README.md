# Marco de análisis — antes de las views

El proyecto vuelve a una base controlada: tablas madre, granularidades y calidad de datos. Todavía no hay views de consumo.

## Preguntas que deberán ramificarse

- Catálogo: cartas, sets, rarezas válidas e impresiones.
- Mercado: precios por carta, marketplace, moneda y snapshot.
- Impresiones: `set_price_usd` por set y rareza.
- Histórico: cobertura y variación entre snapshots comparables.
- Calidad: nulos críticos, duplicados, códigos internos y FK huérfanas.

## Regla de avance

Antes de crear una view se documentará:

```text
pregunta -> tabla fuente -> grano -> PK/FK -> campos -> medida esperada -> riesgo
```

No se volverá a unir precio general con rareza mediante `card_id`.
