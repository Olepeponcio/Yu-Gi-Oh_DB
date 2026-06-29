# Proceso de trabajo en Power BI

Este README documentara el trabajo en Power BI cuando el analisis empiece a generar consultas de consumo.

Documento complementario:

```text
docs/03_powerbi/README_constructor_informe.md
```

Ese README define como usar y mantener `build_powerbi_report.py`, que genera el informe Word y el PNG del modelo.

## Punto de entrada

Power BI se conectara a MySQL:

```text
yugioh_db
```

La conexion no debe alterar las tablas madre. El modelado visual se construira desde las consultas que se vayan definiendo en el proceso de analisis.

## Fondo de pagina inicial

Para la primera pagina de navegacion/cuadro de control:

```text
docs/03_powerbi/assets/fondo_control_powerbi_fondo2.png
```

Uso recomendado:

- Importar el PNG como fondo de pagina.
- Usar transparencia 0%.
- Superponer botones transparentes sobre el bloque reservado de cada marco.
- Configurar cada boton con accion de navegacion a la pagina correspondiente.
- Mantener el texto como guia visual; el bloque lateral del marco queda reservado para el boton.

## Fases de trabajo

| Fase | Entrada | Salida esperada | Estado | Notas |
|---|---|---|---|---|
| Conexion | MySQL `yugioh_db` | Origen configurado | Pendiente | Validar credenciales y tablas disponibles |
| Carga inicial | Tablas madre | Modelo preliminar | Pendiente | No crear relaciones ambiguas |
| Modelo | Consultas documentadas | Relaciones y medidas | Pendiente | Direccion de filtro controlada |
| Visualizacion | Medidas y campos validados | Paginas de informe | Pendiente | Cada pagina debe responder una pregunta |
| Publicacion | Archivo local de trabajo | Plantilla/documentacion | Pendiente | No versionar datos cargados |

## Reglas

- No mezclar monedas sin segmentacion.
- No usar `set_price` como precio de rareza.
- No crear decisiones desde rankings aislados.
- Documentar cada medida relevante.
- Mantener trazabilidad entre visual, consulta y pregunta del diario de analisis.
- Las vistas de hechos agregados se cargan como hechos, no como dimensiones.
- `vw_fact_card_prices_descriptive` es la vista base para precios actuales en formato largo.
- `vw_fact_price_outlier_candidates_diagnostic` debe tratarse como tabla de revision, no como tabla para conclusiones directas.
- No relacionar una vista base de precios con su vista de extremos; una es base y la otra es subconjunto filtrado.

## Vistas de consumo acordadas

| Vista | Tipo | Grano | Uso recomendado |
|---|---|---|---|
| `vw_dim_cards_descriptive` | Dimension | 1 carta | Catalogo base de cartas |
| `vw_dim_sets_descriptive` | Dimension | 1 set | Catalogo de sets |
| `vw_dim_rarities_descriptive` | Dimension | 1 rareza por codigo de impresion | Catalogo tecnico de rarezas |
| `vw_dim_rarity_names_descriptive` | Dimension | 1 nombre de rareza | Relacion con resumen agregado por rareza |
| `vw_dim_marketplaces_descriptive` | Dimension | 1 marketplace | Segmentacion de fuentes de precio |
| `vw_dim_currencies_descriptive` | Dimension | 1 moneda | Segmentacion de precios por moneda |
| `vw_dim_snapshots_descriptive` | Dimension | 1 snapshot | Calendario real de historico disponible |
| `vw_dim_cards_classification` | Lectura descriptiva | 1 combinacion de atributos de carta | Distribucion por tipo |
| `vw_fact_card_set_coverage_descriptive` | Hecho agregado | 1 carta | Cobertura descriptiva de sets |
| `vw_fact_card_prices_descriptive` | Hecho | 1 carta + 1 marketplace + 1 moneda | Precios actuales segmentados |
| `vw_fact_card_set_coverage_diagnostic` | Hecho agregado | 1 carta | Ranking de apariciones/reimpresiones |
| `vw_fact_current_prices_diagnostic` | Hecho | 1 carta + 1 fuente de precio + 1 moneda | Base diagnostica para outliers |
| `vw_fact_rarity_price_summary_diagnostic` | Hecho agregado | 1 rareza | Relacion rareza-precio |
| `vw_fact_price_outlier_candidates_diagnostic` | Hecho filtrado/revision | 1 carta + 1 fuente de precio + 1 moneda | Revision de precios extremos |
| `vw_quality_fk_orphans_diagnostic` | Quality | 1 relacion validada | Control de huerfanos FK |
| `vw_quality_nullable_fk_diagnostic` | Quality | 1 control nullable | Revision de FK opcionales sin resolver |
| `vw_quality_duplicate_grain_diagnostic` | Quality | 1 duplicado de grano | Revision de duplicados en `card_sets` |
| `vw_quality_relationship_summary_diagnostic` | Quality | 1 tabla hija | Resumen de cobertura relacional |
| `vw_fact_price_snapshot_summary_predictive` | Hecho agregado | 1 snapshot | Validar historico disponible |
| `vw_fact_card_price_variation_predictive` | Hecho | 1 carta + 1 marketplace + 1 moneda + 1 snapshot | Analizar variacion temporal de precios |

## Relaciones recomendadas

```text
vw_dim_cards_descriptive 1 -> * vw_fact_card_prices_descriptive
vw_dim_cards_descriptive 1 -> 1 vw_fact_card_set_coverage_diagnostic
vw_dim_cards_descriptive 1 -> * vw_fact_price_outlier_candidates_diagnostic
vw_dim_marketplaces_descriptive 1 -> * vw_fact_card_prices_descriptive
vw_dim_marketplaces_descriptive 1 -> * vw_fact_card_price_variation_predictive
vw_dim_currencies_descriptive 1 -> * vw_fact_card_prices_descriptive
vw_dim_currencies_descriptive 1 -> * vw_fact_card_price_variation_predictive
vw_dim_snapshots_descriptive 1 -> * vw_fact_card_price_variation_predictive
vw_dim_rarity_names_descriptive 1 -> * vw_fact_rarity_price_summary_diagnostic
```

`vw_fact_rarity_price_summary_diagnostic` puede usarse como tabla aislada de resumen si no existe una dimension de rarezas cargada.

Para `vw_fact_current_prices_diagnostic` y `vw_fact_price_outlier_candidates_diagnostic`, la columna equivalente a marketplace se llama `price_source`. Puede relacionarse con `vw_dim_marketplaces_descriptive[marketplace]` si se cargan esas tablas en una pagina de diagnostico.

Nota: la antigua `vw_dim_card_sets_classification` queda normalizada como `vw_fact_card_set_coverage_descriptive` porque contiene metricas agregadas (`total_sets`, `total_appearances`, `total_rarities`).

## Criterio para precios extremos

Vista base:

```text
vw_fact_current_prices_diagnostic
```

Vista derivada:

```text
vw_fact_price_outlier_candidates_diagnostic = subconjunto filtrado de vw_fact_current_prices_diagnostic
```

Uso:

```text
analisis general de precios -> vw_fact_card_prices_descriptive
tabla de control/revision -> vw_fact_price_outlier_candidates_diagnostic
```

## Pagina recomendada: Calidad de datos

Estas vistas se cargan como tablas de control. No necesitan relacionarse con el modelo principal salvo que una visualizacion concreta lo justifique.

| Vista | Visual recomendado | Lectura |
|---|---|---|
| `vw_quality_fk_orphans_diagnostic` | Tabla + tarjetas de suma `issue_count` | `issue_count = 0` correcto; mayor que 0 exige revisar relaciones rotas |
| `vw_quality_nullable_fk_diagnostic` | Tarjetas o tabla simple | Mide FK opcionales sin resolver; no siempre es error |
| `vw_quality_duplicate_grain_diagnostic` | Tabla de detalle | Si aparecen filas, los conteos y medias pueden inflarse |
| `vw_quality_relationship_summary_diagnostic` | Matriz o tabla resumen | Compara `child_rows` y `parent_keys_used` por tabla hija |

Indicadores sugeridos:

```text
Huerfanos FK totales
FK nullable pendientes
Duplicados de grano
Tablas hijas con baja cobertura
```

## Pagina recomendada: Historico de precios

Estas vistas dependen de `card_price_history`. El historico se actualiza con las cargas reales del ETL; Power BI solo consume la foto resultante.

| Vista | Visual recomendado | Lectura |
|---|---|---|
| `vw_fact_price_snapshot_summary_predictive` | Linea temporal + tarjetas | Ver numero de snapshots, cartas cubiertas y continuidad del historico |
| `vw_fact_card_price_variation_predictive` | Linea por carta/marketplace + tabla de variaciones | Comparar precio actual contra snapshot anterior por marketplace y moneda |

Indicadores sugeridos:

```text
Snapshots disponibles
Ultimo snapshot
Cartas con historico comparable
Variacion absoluta
Variacion porcentual
```

## Registro de paginas

| Pagina | Pregunta base | Consulta o tabla usada | Medidas | Estado | Notas |
|---|---|---|---|---|---|
|  |  |  |  | Pendiente |  |

## Registro de medidas

| Medida | Formula o descripcion | Tabla/consulta | Estado | Notas |
|---|---|---|---|---|
|  |  |  | Pendiente |  |
