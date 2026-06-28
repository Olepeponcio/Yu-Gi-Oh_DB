# Power BI

Documentacion de implementacion Power BI asociada al proyecto SQL DB Yu-Gi-Oh.

El marco analitico vive en:

```text
docs/02_marco_analisis_datos/README.md
```

Este README traduce ese marco a conexion, modelo semantico, relaciones, medidas y artefactos Power BI.

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

Power BI debe conectarse a tablas madre de MySQL. No hay capa SQL intermedia oficial en el flujo actual.

Tablas base cargables:

```text
cards
sets
rarities
card_sets
card_images
card_prices
card_price_history
card_banlist
card_typelines
card_linkmarkers
```

## Modelo semantico

Power BI es ahora la capa donde se construyen dimensiones, hechos y medidas.

Dimensiones candidatas:

```text
DimCard              <- cards
DimSet               <- sets
DimRarity            <- rarities
DimMarketplace       <- derivada de marketplaces de precios
DimBanlistFormat     <- TCG, OCG, GOAT
Calendario           <- derivada de card_price_history[snapshot_at]
```

Hechos candidatos:

```text
FactCardSetPrintings <- card_sets
FactPricesCurrent    <- card_prices despivotado por marketplace
FactPricesHistory    <- card_price_history despivotado por marketplace y snapshot
FactBanlistStatus    <- card_banlist despivotado por formato
FactTypelines        <- card_typelines si se analiza typeline
```

## Relaciones recomendadas

```text
DimCard[card_id] 1 -> * FactCardSetPrintings[card_id]
DimSet[set_id] 1 -> * FactCardSetPrintings[set_id]
DimRarity[rarity_id] 1 -> * FactCardSetPrintings[rarity_id]

DimCard[card_id] 1 -> * FactPricesCurrent[card_id]
DimMarketplace[marketplace] 1 -> * FactPricesCurrent[marketplace]

DimCard[card_id] 1 -> * FactPricesHistory[card_id]
DimMarketplace[marketplace] 1 -> * FactPricesHistory[marketplace]
Calendario[Date] 1 -> * FactPricesHistory[snapshot_date]

DimCard[card_id] 1 -> * FactBanlistStatus[card_id]
DimBanlistFormat[format] 1 -> * FactBanlistStatus[format]
```

Direccion de filtro: unica, desde dimension hacia hecho.

Evitar relaciones bidireccionales salvo necesidad concreta de pagina.

## Calendario

La dimension temporal se crea en Power BI.

Documento:

```text
powerbi/consultas/tabla_calendario_dax.md
```

Relacion prevista:

```text
Calendario[Date] 1 -> * FactPricesHistory[snapshot_date]
```

## Monedas y medidas base

No mezclar monedas sin conversion o segmentacion visible.

Origenes:

```text
card_prices          -> precios actuales por marketplace
card_price_history   -> historico por snapshot ETL
card_sets.set_price  -> precio de aparicion de carta en set
```

Regla central:

```text
set_price no es precio de rareza.
set_price pertenece a la aparicion carta + set + rareza.
```

Medidas base sugeridas:

```DAX
Precio medio = AVERAGE(FactPricesCurrent[price])
Precio maximo = MAX(FactPricesCurrent[price])
Total observaciones precio = COUNTROWS(FactPricesCurrent)
Precio historico medio = AVERAGE(FactPricesHistory[price])
Snapshots = DISTINCTCOUNT(FactPricesHistory[snapshot_at])
Total impresiones = COUNTROWS(FactCardSetPrintings)
```

## Paginas recomendadas

| Pagina | Base de datos | Accion esperada |
|---|---|---|
| Catalogo | `cards`, `sets`, `rarities`, `card_sets` | Entender cobertura y segmentar cartas. |
| Precio actual | `card_prices`, `cards` | Priorizar cartas por valor observado. |
| Rareza y set | `card_sets`, `sets`, `rarities` | Revisar impacto de set/rareza sin confundirlo con precio de rareza. |
| Calidad | queries diagnosticas sobre tablas base | Revisar extremos y datos incompletos. |
| Mercado | medidas Power BI sobre precios e impresiones | Detectar arquetipos o cartas con interes estimado. |
| Decision comercial | medidas y columnas DAX validadas | Clasificar cartas candidatas por accion comercial. |
| Historico | `card_price_history`, `Calendario` | Vigilar variacion cuando haya snapshots suficientes. |

## Estado de trabajo

Punto actual:

```text
fuente unica MySQL relacional
modelo semantico pendiente de reconstruccion en Power BI
reglas comerciales pendientes de validacion
```

Las clasificaciones comerciales deben construirse como medidas o columnas calculadas en Power BI hasta que demuestren utilidad.

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
