# Power BI

Documentacion y artefactos ligeros del trabajo de Power BI asociado al proyecto.

Estado actual: pausado. El trabajo activo vuelve a MySQL `yugioh_db` para consolidar la capa SQL semantica y diagnostica antes de retomar el modelo en Power BI.

## Estructura

```text
modelos/       -> plantillas .pbit versionables; no subir .pbix por defecto
consultas/     -> SQL, Power Query M y medidas DAX documentadas
capturas/      -> capturas ligeras del modelo, relaciones o informes
exportaciones/ -> salidas locales generadas; ignoradas por Git salvo .gitkeep
```

## Conexion recomendada futura

Origen: MySQL local.

```text
Servidor: localhost:3306
Base de datos: yugioh_db
Conector: Base de datos MySQL
Modo recomendado: Importar
```

Usar `Importar` como modo principal porque el origen es local, mejora el rendimiento del modelo y permite trabajar con mas libertad en Power BI. Usar `DirectQuery` solo si el informe necesita consultar datos en vivo desde MySQL y se aceptan limitaciones de rendimiento y modelado.

## Flujo de trabajo futuro

Cuando se retome Power BI:

1. Abrir Power BI Desktop.
2. Seleccionar `Inicio > Obtener datos > Base de datos MySQL`.
3. Conectar contra `localhost:3306` y la base `yugioh_db`.
4. Seleccionar views preparadas para Power BI, no tablas base.
5. Construir el modelo en estrella con dimensiones y hechos.
6. Guardar una plantilla `.pbit` en `modelos/`.
7. Documentar consultas SQL, Power Query M o medidas DAX en `consultas/`.
8. Guardar exportaciones locales solo en `exportaciones/`.

## Modelo relacional objetivo futuro

Power BI debera consumir una capa semantica de views MySQL:

```text
vw_dim_card
vw_dim_set
vw_dim_rarity
vw_ref_banlist_status

vw_bridge_card_set
vw_fact_card_prices
vw_fact_price_history
vw_agg_card_price_current
```

Relaciones esperadas:

```text
vw_dim_card[card_id] 1 -> * vw_bridge_card_set[card_id]
vw_dim_set[set_id] 1 -> * vw_bridge_card_set[set_id]
vw_dim_rarity[rarity_id] 1 -> * vw_bridge_card_set[rarity_id]
vw_dim_card[card_id] 1 -> * vw_fact_card_prices[card_id]
vw_dim_card[card_id] 1 -> * vw_fact_price_history[card_id]
vw_dim_date[date] 1 -> * vw_fact_price_history[snapshot_date]
```

Direccion de filtro recomendada: de dimension a hecho. Evitar relaciones bidireccionales salvo justificacion.

## Views y consultas localizadas

Usar como base o referencia:

```text
sql/analysis/views/vw_fact_card_prices.sql
```

Usar como diagnostico auxiliar:

```text
sql/analysis/views/diagnostic/vw_diag_competitive_staple_candidates.sql
sql/analysis/views/diagnostic/vw_diag_high_demand_archetypes.sql
sql/analysis/views/diagnostic/vw_diag_price_by_rarity.sql
sql/analysis/views/diagnostic/vw_diag_price_outliers.sql
```

Convertir manualmente en view si entra en el informe:

```text
sql/analysis/queries/diagnostic/q_diag_price_variation_usd.sql
```

Las `vw_diag_*` no deben ser el nucleo relacional del modelo. Sirven para validacion, paginas diagnosticas o comparacion con medidas DAX.

## Tabla de trabajo SQL -> Power BI

| Nombre de view | Uso en Power BI |
|---|---|
| `vw_dim_card` | Filtros y atributos de carta. |
| `vw_dim_set` | Filtros por set o expansion. |
| `vw_dim_rarity` | Segmentacion por rareza. |
| `vw_ref_banlist_status` | Filtro de legalidad competitiva. |
| `vw_bridge_card_set` | Relacionar cartas con impresiones, sets y rarezas. |
| `vw_fact_card_prices` | Medidas de precio actual por marketplace. |
| `vw_fact_price_history` | Tendencias por snapshot historico. |
| `vw_agg_card_price_current` | Rankings rapidos de valor actual. |
| `vw_diag_price_outliers` | Pagina auxiliar de control de calidad. |

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
