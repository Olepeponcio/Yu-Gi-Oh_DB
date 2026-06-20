# Tabla calendario DAX

Ultima actualizacion: 2026-06-20.

## Finalidad

Crear una dimension temporal dentro de Power BI para analizar `vw_fact_price_history` por fecha de snapshot.

La tabla calendario no se crea en MySQL. Se crea como tabla calculada DAX en Power BI y se marca como tabla de fechas.

## Tabla calculada

```DAX
Calendario =
CALENDAR (
    MIN ( vw_fact_price_history[snapshot_date] ),
    MAX ( vw_fact_price_history[snapshot_date] )
)
```

## Columnas calculadas recomendadas

```DAX
Año = YEAR ( Calendario[Date] )
```

```DAX
Mes Numero = MONTH ( Calendario[Date] )
```

```DAX
Mes = FORMAT ( Calendario[Date], "MMMM" )
```

```DAX
Año Mes = FORMAT ( Calendario[Date], "YYYY-MM" )
```

```DAX
Trimestre = "T" & FORMAT ( Calendario[Date], "Q" )
```

## Relacion del modelo

```text
Calendario[Date] 1 -> * vw_fact_price_history[snapshot_date]
```

Direccion de filtro cruzado:

```text
Unico
```

## Configuracion en Power BI

1. Crear la tabla calculada `Calendario`.
2. Crear las columnas calculadas necesarias.
3. Seleccionar la tabla `Calendario`.
4. Ir a `Herramientas de tabla > Marcar como tabla de fechas`.
5. Elegir la columna `Calendario[Date]`.
6. Crear la relacion con `vw_fact_price_history[snapshot_date]`.

## Criterio

Usar `snapshot_date` para la relacion diaria.

No usar `snapshot_at` para la tabla calendario salvo que se quiera analizar la hora exacta de ejecucion del ETL.
