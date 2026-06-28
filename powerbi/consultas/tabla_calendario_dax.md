# Tabla calendario DAX

## Objetivo

Crear una dimension temporal dentro de Power BI para analizar `card_price_history` por fecha de snapshot.

La tabla calendario no se crea en MySQL. Se crea como tabla calculada DAX en Power BI y se marca como tabla de fechas.

## DAX base

Cuando `FactPricesHistory` ya exista en Power BI:

```DAX
Calendario =
CALENDAR (
    MIN ( FactPricesHistory[snapshot_date] ),
    MAX ( FactPricesHistory[snapshot_date] )
)
```

Columnas recomendadas:

```DAX
Ano = YEAR ( Calendario[Date] )
Mes numero = MONTH ( Calendario[Date] )
Mes = FORMAT ( Calendario[Date], "MMMM" )
Ano mes = FORMAT ( Calendario[Date], "YYYY-MM" )
Trimestre = "T" & FORMAT ( Calendario[Date], "Q" )
Dia = DAY ( Calendario[Date] )
```

Relacion prevista:

```text
Calendario[Date] 1 -> * FactPricesHistory[snapshot_date]
```

## Nota

`FactPricesHistory` es una tabla semantica de Power BI derivada de `card_price_history`, normalmente despivotando marketplaces.
