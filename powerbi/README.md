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
| Decision comercial | `vw_diag_competitive_staple_candidates` | Clasificar cartas candidatas por accion comercial. |
| Historico | `vw_fact_price_history`, `Calendario` | Vigilar variacion cuando haya snapshots suficientes. |

## Avance de paginas

Bloques cerrados:

```text
descriptivo
diagnostico
```

Evidencias:

```text
powerbi/exportaciones/analisis_desc_diag
docs/02_marco_analisis_datos/informes/informe_conclusiones_desc_diag.md
docs/02_marco_analisis_datos/informes/informe_conclusiones_desc_diag.docx
```

Pagina prescriptiva activa:

```text
decision comercial
```

Visuales actuales:

- Tabla principal de cartas candidatas.
- Segmentador por `clasificacion_comercial`.
- Grafico de distribucion de cartas por clasificacion.
- Resumen visual de clasificaciones.
- Texto de lectura: reglas conservadoras, primera version prescriptiva.

## Columnas DAX prescriptivas

Tabla base:

```text
yugioh_db vw_diag_competitive_staple_candidates
```

Columnas creadas en Power BI:

```DAX
clasificacion_comercial =
SWITCH(
    TRUE(),

    'yugioh_db vw_diag_competitive_staple_candidates'[avg_set_price] >= 50
        && 'yugioh_db vw_diag_competitive_staple_candidates'[total_printings] >= 20,
        "Carta principal potencial",

    'yugioh_db vw_diag_competitive_staple_candidates'[avg_set_price] >= 5
        && 'yugioh_db vw_diag_competitive_staple_candidates'[total_printings] >= 10,
        "Carta destacada comercial",

    'yugioh_db vw_diag_competitive_staple_candidates'[avg_set_price] < 5
        && 'yugioh_db vw_diag_competitive_staple_candidates'[total_printings] >= 20,
        "Carta complementaria",

    "Revisar antes de accionar"
)
```

```DAX
motivo_clasificacion =
SWITCH(
    'yugioh_db vw_diag_competitive_staple_candidates'[clasificacion_comercial],

    "Carta principal potencial",
        "Precio medio alto y alta presencia en impresiones.",

    "Carta destacada comercial",
        "Precio relevante y presencia suficiente para destacar.",

    "Carta complementaria",
        "Precio bajo o moderado con alta disponibilidad.",

    "Revisar antes de accionar",
        "No cumple criterios suficientes o requiere validacion adicional."
)
```

Uso:

- `clasificacion_comercial` etiqueta la accion comercial.
- `motivo_clasificacion` explica por que la carta cae en esa categoria.
- El segmentador permite revisar cada grupo sin duplicar tablas.
- Las reglas siguen en validacion; no deben consolidarse como view SQL hasta comprobar que clasifican de forma util.

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
