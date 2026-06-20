# Power BI

Documentacion y artefactos ligeros del trabajo de Power BI asociado al proyecto.

Estado actual: activo. El modelo ya consume views de MySQL `yugioh_db` y se esta construyendo como capa narrativa sobre precios, rarezas, sets, arquetipos y posibles cartas de interes comercial.

## Estructura

```text
modelos/       -> plantillas .pbit versionables; no subir .pbix por defecto
consultas/     -> SQL, Power Query M y medidas DAX documentadas
capturas/      -> capturas ligeras del modelo, relaciones o informes
exportaciones/ -> salidas locales generadas; ignoradas por Git salvo .gitkeep
```

## Conexion actual

Origen: MySQL local.

```text
Servidor: localhost:3306
Base de datos: yugioh_db
Conector: Base de datos MySQL
Modo recomendado: Importar
```

Usar `Importar` como modo principal porque el origen es local, mejora el rendimiento del modelo y permite trabajar con mas libertad en Power BI. Usar `DirectQuery` solo si el informe necesita consultar datos en vivo desde MySQL y se aceptan limitaciones de rendimiento y modelado.

## Views del modelo

Segun el estado actual del modelo Power BI, las views cargadas son:

```text
vw_dim_card
vw_dim_set
vw_dim_rarity
vw_bridge_card_set
vw_bridge_card_banlist
vw_fact_card_prices
vw_fact_price_history
vw_ref_banlist_status
vw_diag_price_by_rarity
vw_diag_price_outliers
vw_diag_high_demand_archetypes
vw_diag_competitive_staple_candidates
```

El nucleo relacional debe apoyarse en `vw_dim_*`, `vw_bridge_*`, `vw_fact_*` y, si se relaciona correctamente, `vw_ref_banlist_status`.

Las `vw_diag_*` no son el nucleo del modelo en estrella. Sirven para paginas de diagnostico, validacion y narrativa analitica.

## Modelo relacional actual

Relaciones principales recomendadas:

```text
vw_dim_card[card_id] 1 -> * vw_bridge_card_set[card_id]
vw_dim_set[set_id] 1 -> * vw_bridge_card_set[set_id]
vw_dim_rarity[rarity_id] 1 -> * vw_bridge_card_set[rarity_id]
vw_dim_card[card_id] 1 -> * vw_bridge_card_banlist[card_id]
vw_ref_banlist_status[banlist_status_key] 1 -> * vw_bridge_card_banlist[banlist_status_key]

vw_dim_card[card_id] 1 -> * vw_fact_card_prices[card_id]
vw_dim_card[card_id] 1 -> * vw_fact_price_history[card_id]
```

Direccion de filtro recomendada: unica, desde dimension hacia bridge/hecho.

Evitar relaciones bidireccionales salvo que una pagina concreta lo justifique. Si una visual necesita cruzar set, rareza y precio, partir de `vw_bridge_card_set` y medidas DAX controladas suele ser mas claro que forzar filtros bidireccionales.

## Relaciones auxiliares

No crear automaticamente relaciones que parezcan posibles si no hay una clave estable.

```text
vw_ref_banlist_status y vw_bridge_card_banlist
```

`vw_ref_banlist_status` normaliza estados de banlist por `format` y `ban_status`. `vw_bridge_card_banlist` conecta esos estados con cartas mediante `card_id`.

La relacion entre referencia y puente esta cargada mediante `banlist_status_key`, porque Power BI trabaja mejor con una sola clave que con claves compuestas.

```text
Tabla calendario en Power BI
```

La dimension temporal no se creara como view SQL. Se creara en Power BI como tabla calculada DAX y se establecera como tabla de fechas.

La definicion DAX queda documentada en `powerbi/consultas/tabla_calendario_dax.md`.

La relacion prevista sera:

```text
Calendario[Date] 1 -> * vw_fact_price_history[snapshot_date]
```

Hasta crearla, usar `snapshot_date` directamente solo como solucion temporal.

```text
vw_agg_card_price_current
```

No existe en el estado actual cargado. Si se necesita ranking rapido por carta, puede resolverse primero con medidas DAX sobre `vw_fact_card_prices` antes de crear una view agregada.

## Monedas y medidas

No mezclar monedas en una misma medida sin conversion explicita.

Estado actual de facts:

```text
vw_fact_card_prices   -> precios actuales por marketplace en USD
vw_fact_price_history -> historico con cardmarket en EUR y otros marketplaces en USD
```

Medidas recomendadas base:

```DAX
Precio medio = AVERAGE(vw_fact_card_prices[price])
Precio maximo = MAX(vw_fact_card_prices[price])
Total observaciones precio = COUNTROWS(vw_fact_card_prices)
```

Para historico:

```DAX
Precio historico medio = AVERAGE(vw_fact_price_history[price])
Snapshots = DISTINCTCOUNT(vw_fact_price_history[snapshot_at])
```

En visuales monetarias, filtrar siempre por `currency` o mostrar la moneda en leyenda/segmentador.

## Narrativa analitica recomendada

El informe debe contar una historia, no solo listar tablas.

Las preguntas marco no se redefinen aqui. La fuente canonica es `docs/02_marco_analisis_datos/README.md`; este documento solo traduce esas preguntas a bloques de informe, relaciones y medidas.

Marco narrativo:

```text
1. Vision general del catalogo
2. Precio actual por carta y marketplace
3. Impacto de set y rareza
4. Diagnostico de outliers y calidad
5. Arquetipos con peso de mercado
6. Candidatas competitivas o comerciales
7. Evolucion temporal cuando haya suficientes snapshots
```

Uso de views por bloque:

| Bloque | Views principales | Para que sirve |
|---|---|---|
| Catalogo | `vw_dim_card`, `vw_dim_set`, `vw_dim_rarity`, `vw_bridge_card_set` | Entender que cartas, sets y rarezas existen. |
| Precio actual | `vw_fact_card_prices`, `vw_dim_card` | Comparar cartas y marketplaces actuales. |
| Historico | `vw_fact_price_history`, `vw_dim_card` | Ver variacion por ejecucion del ETL. |
| Rareza | `vw_diag_price_by_rarity`, `vw_dim_rarity` | Diagnosticar si la rareza explica diferencias de precio. |
| Calidad | `vw_diag_price_outliers` | Detectar precios extremos antes de concluir. |
| Mercado | `vw_diag_high_demand_archetypes` | Identificar arquetipos con peso estimado. |
| Decision | `vw_diag_competitive_staple_candidates` | Proponer cartas candidatas para destacar. |

Bloques auxiliares de la narrativa:

| Bloque | Motivo |
|---|---|
| `vw_diag_price_outliers` | Control de calidad antes de concluir sobre precios extremos. |
| `vw_diag_high_demand_archetypes` | Amplia la pregunta de sets/cartas hacia peso de mercado por arquetipo. |
| `vw_diag_competitive_staple_candidates` | Conecta con la decision de destacar cartas candidatas. |
| `vw_bridge_card_banlist` + `vw_ref_banlist_status` | Permite segmentar cartas por legalidad competitiva. |

## Tabla SQL -> Power BI

| Nombre de view | Uso en Power BI | Estado |
|---|---|---|
| `vw_dim_card` | Filtros y atributos de carta. | Cargada |
| `vw_dim_set` | Filtros por set o expansion. | Cargada |
| `vw_dim_rarity` | Segmentacion por rareza. | Cargada |
| `vw_bridge_card_set` | Relacionar cartas con impresiones, sets y rarezas. | Cargada |
| `vw_bridge_card_banlist` | Relacionar cartas con estado de banlist por formato. | Cargada y relacionada |
| `vw_fact_card_prices` | Medidas de precio actual por marketplace. | Cargada |
| `vw_fact_price_history` | Tendencias por snapshot historico. | Cargada |
| `vw_ref_banlist_status` | Catalogo de estados de legalidad. | Cargada y relacionada |
| `vw_diag_price_by_rarity` | Diagnostico de precio por rareza. | Cargada |
| `vw_diag_price_outliers` | Control de calidad de precios extremos. | Cargada |
| `vw_diag_high_demand_archetypes` | Arquetipos con peso estimado de mercado. | Cargada |
| `vw_diag_competitive_staple_candidates` | Cartas candidatas por precio y reimpresiones. | Cargada |
| `vw_agg_card_price_current` | Ranking rapido de valor actual. | No creada |
| Tabla calculada `Calendario` | Calendario para historico; debe marcarse como tabla de fechas en Power BI. | Pendiente en Power BI |

## Politica de versionado

Versionar:

- Documentacion Markdown.
- Consultas SQL.
- Codigo Power Query M o DAX.
- Capturas ligeras utiles para explicar el modelo.
- Plantillas `.pbit` sin datos cargados.

No versionar por defecto:

- Archivos `.pbix`.
- Exportaciones `.csv` o `.xlsx`.
- Datos locales generados desde Power BI.
