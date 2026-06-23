# Power BI

Documentacion de implementacion Power BI asociada al proyecto SQL DB Yu-Gi-Oh.

El marco analitico vive en:

```text
docs/02_marco_analisis_datos/README.md
```

Este README solo traduce ese marco a modelo, relaciones, medidas y artefactos Power BI.

## Estructura

```text
modelos/       -> plantillas .pbit versionables; no subir .pbix por defecto
consultas/     -> SQL, Power Query M y medidas DAX documentadas
capturas/      -> capturas ligeras del modelo, relaciones o informes
exportaciones/ -> salidas locales generadas; ignoradas por Git salvo .gitkeep
```

## Conexion

```text
Origen: MySQL local
Servidor: localhost:3306
Base de datos: yugioh_db
Modo recomendado: Importar
```

Usar `Importar` como modo principal. `DirectQuery` solo tiene sentido si el informe necesita datos en vivo y acepta limitaciones de rendimiento/modelado.

## Views cargables

Nucleo relacional:

```text
vw_dim_card
vw_dim_set
vw_dim_rarity
vw_bridge_card_set
vw_bridge_card_banlist
vw_fact_card_prices
vw_fact_price_history
vw_ref_banlist_status
```

Soporte visual o auxiliar:

```text
vw_dim_card_image
vw_dim_card_typelines
```

Diagnostico y narrativa:

```text
vw_diag_price_by_rarity
vw_diag_price_outliers
vw_diag_high_demand_archetypes
vw_diag_competitive_staple_candidates
```

Las `vw_diag_*` sirven para paginas de diagnostico, validacion y recomendacion. No deben forzar relaciones bidireccionales en el nucleo del modelo.

## Relaciones recomendadas

```text
vw_dim_card[card_id] 1 -> * vw_bridge_card_set[card_id]
vw_dim_set[set_id] 1 -> * vw_bridge_card_set[set_id]
vw_dim_rarity[rarity_id] 1 -> * vw_bridge_card_set[rarity_id]
vw_dim_card[card_id] 1 -> * vw_bridge_card_banlist[card_id]
vw_ref_banlist_status[banlist_status_key] 1 -> * vw_bridge_card_banlist[banlist_status_key]
vw_dim_card[card_id] 1 -> * vw_fact_card_prices[card_id]
vw_dim_card[card_id] 1 -> * vw_fact_price_history[card_id]
```

Direccion de filtro: unica, desde dimension hacia bridge/hecho.

Evitar relaciones bidireccionales salvo necesidad concreta de pagina.

## Calendario

La dimension temporal se crea en Power BI, no como view SQL.

Documento:

```text
powerbi/consultas/tabla_calendario_dax.md
```

Relacion prevista:

```text
Calendario[Date] 1 -> * vw_fact_price_history[snapshot_date]
```

## Monedas y medidas base

No mezclar monedas sin conversion o segmentacion visible.

```text
vw_fact_card_prices   -> precios actuales por marketplace
vw_fact_price_history -> historico por snapshot ETL
```

Medidas base:

```DAX
Precio medio = AVERAGE(vw_fact_card_prices[price])
Precio maximo = MAX(vw_fact_card_prices[price])
Total observaciones precio = COUNTROWS(vw_fact_card_prices)
Precio historico medio = AVERAGE(vw_fact_price_history[price])
Snapshots = DISTINCTCOUNT(vw_fact_price_history[snapshot_at])
```

En visuales monetarias, filtrar por `currency` o mostrar moneda en leyenda/segmentador.

## Paginas recomendadas

| Pagina | Views principales | Accion esperada |
|---|---|---|
| Catalogo | `vw_dim_card`, `vw_dim_set`, `vw_dim_rarity`, `vw_bridge_card_set` | Entender cobertura y segmentar cartas. |
| Precio actual | `vw_fact_card_prices`, `vw_dim_card` | Priorizar cartas por valor observado. |
| Rareza y set | `vw_bridge_card_set`, `vw_dim_set`, `vw_dim_rarity`, `vw_diag_price_by_rarity` | Justificar impacto de rareza o expansion. |
| Calidad | `vw_diag_price_outliers` | Revisar precios extremos antes de recomendar. |
| Mercado | `vw_diag_high_demand_archetypes` | Detectar arquetipos con peso estimado. |
| Decision comercial | `vw_diag_competitive_staple_candidates` | Proponer cartas candidatas para destacar. |
| Historico | `vw_fact_price_history`, `Calendario` | Vigilar variacion cuando haya snapshots suficientes. |

## Politica de versionado

Versionar:

- Documentacion Markdown.
- Consultas SQL.
- Codigo Power Query M o DAX.
- Capturas ligeras utiles.
- Plantillas `.pbit` sin datos cargados.

No versionar por defecto:

- Archivos `.pbix`.
- Exportaciones `.csv` o `.xlsx`.
- Datos locales generados desde Power BI.
