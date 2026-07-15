# Registro modular de diseño de views

Este árbol es el contrato anterior al SQL. Una view solo se implementa después de completar su ficha y aprobar su granularidad.

## Ramas

```text
view_design/
├── 01_descriptive/README.md
├── 02_diagnostic/README.md
├── 03_predictive/README.md
└── 04_prescriptive/README.md
```

Orden de madurez:

```text
descriptive → diagnostic → predictive → prescriptive
```

El orden expresa dependencia de conocimiento, no obliga a crear una view para cada pregunta. Si una medida DAX sobre una view base resuelve correctamente la cuestión, no se añade otra view.

## Preguntas maestras reducidas

Estas son las cuestiones que gobiernan el modelo. Las preguntas técnicas restantes existen únicamente para validar grano y calidad.

| Bloque | Pregunta principal | Decisión que habilita |
|---|---|---|
| Vista general | ¿Qué volumen de cartas, sets, rarezas válidas y marketplaces contiene el modelo, y qué monedas/snapshots condicionan su lectura? | Determinar cobertura y contexto del panel |
| Descriptive | ¿Qué cartas tienen mayor precio vigente por marketplace y qué sets concentran mayor valor de impresión? | Identificar distribuciones y concentraciones relevantes |
| Diagnostic | ¿Qué rarezas válidas se asocian con precios de impresión más altos y qué cartas concentran más reimpresiones? | Explicar diferencias sin cruzar granos incompatibles |
| Predictive | ¿Qué series muestran variaciones o tendencias relevantes entre snapshots comparables? | Seleccionar movimientos que merecen seguimiento |
| Prescriptive | ¿Qué señales validadas justifican seguimiento y cuáles deben quedar en revisión? | Priorizar revisión humana, no recomendar automáticamente |
| Calidad transversal | ¿Existen huérfanos, duplicados, valores internos o baja cobertura que invaliden la interpretación? | Autorizar o bloquear el uso analítico de los datos |

No se añadirá una pregunta nueva si puede resolverse como desglose, filtro o medida de una pregunta maestra existente.

## Plantilla obligatoria

Cada candidata se documentará así:

```markdown
### <nombre_provisional>

- Módulo:
- Estado: propuesta | aprobada | implementada | validada | retirada
- Pregunta de negocio:
- Decisión que habilita:
- Tablas de única verdad:
- Grano —una fila representa—:
- Clave única esperada:
- FK expuestas:
- Campos descriptivos:
- Medidas físicas:
- Filtros de calidad:
- Nulos admitidos:
- Moneda y tiempo:
- Relaciones Power BI:
- Medidas DAX consumidoras:
- Riesgo semántico:
- Consulta de control:
- Criterio de aceptación:
```

## Reglas comunes

1. Una view declara un único grano.
2. Una columna descriptiva no sustituye su FK.
3. No relacionar hechos entre sí.
4. No atribuir precio general de carta a set o rareza.
5. `set_price_usd` es el único precio actual atribuible a una impresión.
6. `card_price_history.price` pertenece a carta, marketplace, moneda y snapshot.
7. No mezclar EUR/USD en una medida sin conversión explícita.
8. Los agregados, rankings y outliers son preferentemente medidas DAX.
9. Toda view debe devolver cero duplicados de su clave declarada.
10. Toda FK obligatoria debe devolver cero huérfanos.
11. Los valores raw se conservan para auditoría, no para filtrar el modelo principal.
12. La dirección prevista en Power BI es `dimensión 1 → * hecho`.

## Convención de nombres

```text
vw_dim_<entidad>           dimensión conformada
vw_fact_<proceso>          observaciones medibles
vw_bridge_<relacion>       relación muchos-a-muchos justificada
vw_dq_<control>            control de calidad, fuera del modelo principal
```

Los nombres `descriptive`, `diagnostic`, `predictive` y `prescriptive` organizan preguntas; no se añaden al nombre si duplican el significado de la entidad.

## Flujo por cada view

```text
formular pregunta
→ completar ficha
→ comprobar fuente y grano
→ aprobar claves/relaciones
→ escribir SQL aislado en sql/views/<módulo>/
→ añadir controles
→ probar datos reales
→ registrar uso en Power BI
```

## Definition of Done

- SQL idempotente mediante `CREATE OR REPLACE VIEW`.
- Sin `ORDER BY` decorativo.
- Grano y claves documentados.
- Controles de duplicados, nulos y huérfanos ejecutados.
- Moneda y snapshot explícitos cuando exista precio.
- Relación Power BI sin ambigüedad.
- README del módulo actualizado a estado `validada`.
