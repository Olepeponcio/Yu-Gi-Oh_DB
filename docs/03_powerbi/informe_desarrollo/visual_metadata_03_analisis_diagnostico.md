# Metadatos visual: suma total por set y rareza

## Ubicacion

```text
Archivo: power_bi/informes/analisis_yugioh_db.pbix
Pagina: 03_Análisis_diagnostico
Visual: lineChart
Titulo: Suma total por set y rareza
```

## Campos detectados

| Rol visual | Campo / medida | Tabla | Agregacion |
|---|---|---|---|
| Eje X | rarity_name | yugioh_db vw_fact_card_set_appearances | categoria |
| Eje Y | set_price | yugioh_db vw_fact_card_set_appearances | suma |
| Eje Y | avg_price_USD | yugioh_db vw_fact_avg_market_price | suma |
| Eje Y secundario | sesgo media Vs mediana | _Medidas_analisis_diagnostico | medida |

## Filtros y ordenacion

```text
Filtro detectado: marketplace = cardmarket
Ordenacion: Suma de set_price descendente
```

## Medidas referenciadas en la pagina diagnostica

| Medida | Tabla de medidas |
|---|---|
| Apariciones en Sets | _Medidas_analisis_diagnostico |
| Precio Mediano por Rareza | _Medidas_analisis_diagnostico |
| Sets Distintos por Carta | _Medidas_analisis_diagnostico |
| sesgo media Vs mediana | _Medidas_analisis_diagnostico |

## Riesgo de lectura

El visual mezcla suma de precio de set, suma de precio medio USD y sesgo en eje secundario. Para una pregunta sobre rarezas asociadas a precios altos, la suma puede confundir precio con volumen de registros.

## Recomendacion

Usar mediana como valor principal y dejar media/sesgo como diagnostico:

```text
Eje X: rarity_name
Eje Y: Precio Mediano por Rareza
Tooltip: Precio Medio, Precio Mediano, Sesgo Media vs Mediana, Sesgo %
Orden: Precio Mediano descendente
```
