# Proceso de trabajo en Power BI

Power BI se conectara a MySQL:

```text
yugioh_db
```

La conexion no debe alterar las tablas madre. El informe debe cargarse desde las vistas `vw_` del modelo relacional simplificado.

## Fondo de pagina inicial

Para la primera pagina de navegacion/cuadro de control:

```text
power_bi/assets/fondo_control_powerbi_fondo2.png
```

## Archivos Power BI

```text
docs/03_powerbi/modelo_relacional.svg          -> modelo relacional de referencia
power_bi/assets/                               -> fondos e imagenes de diseno
power_bi/informes/analisis_yugioh_db.pbix      -> informe Power BI del proyecto
```

## Reglas

- No mezclar monedas sin segmentacion o conversion.
- No usar `set_price` como precio propio de una rareza.
- No crear decisiones desde rankings aislados.
- Documentar cada medida relevante.
- Mantener trazabilidad entre visual, vista SQL y pregunta.
- Cargar dimensiones y hechos base; los rankings, outliers y resumenes se calculan como medidas o visuales desde esas tablas.
- Usar filtro unico desde dimensiones hacia hechos.

## Vistas de consumo acordadas

| Vista | Tipo | Grano | Uso recomendado |
|---|---|---|---|
| `vw_dim_cards_descriptive` | Dimension | 1 carta | Catalogo base de cartas |
| `vw_dim_sets_descriptive` | Dimension | 1 set | Catalogo de sets |
| `vw_dim_rarities_descriptive` | Dimension | 1 rareza por codigo de impresion | Catalogo tecnico de rarezas |
| `vw_dim_marketplaces_descriptive` | Dimension | 1 marketplace | Segmentacion de fuentes de precio |
| `vw_dim_currencies_descriptive` | Dimension | 1 moneda | Segmentacion de precios por moneda |
| `vw_dim_snapshots_descriptive` | Dimension temporal | 1 snapshot | Calendario real de historico disponible |
| `vw_fact_card_prices_descriptive` | Hecho | 1 carta + 1 marketplace + 1 moneda | Precios actuales segmentados |
| `vw_fact_card_set_appearances` | Hecho puente | 1 carta + 1 set + 1 rareza | Apariciones, reimpresiones y precio de set |
| `vw_fact_card_price_variation_predictive` | Hecho historico | 1 carta + 1 marketplace + 1 moneda + 1 snapshot | Variacion temporal de precios |

## Relaciones recomendadas

```text
vw_dim_cards_descriptive 1 -> * vw_fact_card_prices_descriptive
vw_dim_cards_descriptive 1 -> * vw_fact_card_set_appearances
vw_dim_cards_descriptive 1 -> * vw_fact_card_price_variation_predictive
vw_dim_sets_descriptive 1 -> * vw_fact_card_set_appearances
vw_dim_rarities_descriptive 1 -> * vw_fact_card_set_appearances
vw_dim_marketplaces_descriptive 1 -> * vw_fact_card_prices_descriptive
vw_dim_marketplaces_descriptive 1 -> * vw_fact_card_price_variation_predictive
vw_dim_currencies_descriptive 1 -> * vw_fact_card_prices_descriptive
vw_dim_currencies_descriptive 1 -> * vw_fact_card_price_variation_predictive
vw_dim_snapshots_descriptive 1 -> * vw_fact_card_price_variation_predictive
```

## Paginas previstas

Indice de trabajo para Power BI Desktop: 6 paginas. El foco actual esta en las paginas 1 a 5; la pagina 6 queda como control de calidad antes de cerrar interpretaciones.

| Orden | Pagina | Preguntas guia | Vistas base | Estado |
|---|---|---|---|---|
| 1 | Vista general | Que volumen de cartas, sets, rarezas y marketplaces contiene el modelo? Que monedas y snapshots condicionan la lectura del panel? | `vw_dim_cards_descriptive`, `vw_dim_sets_descriptive`, `vw_dim_rarities_descriptive`, `vw_dim_marketplaces_descriptive`, `vw_dim_currencies_descriptive`, `vw_dim_snapshots_descriptive` | Foco actual |
| 2 | Analisis descriptivo | Que cartas tienen mayor precio medio por marketplace? Que sets concentran mayor valor de mercado? | `vw_fact_card_prices_descriptive`, `vw_fact_card_set_appearances`, `vw_dim_sets_descriptive`, `vw_dim_marketplaces_descriptive`, `vw_dim_currencies_descriptive` | Foco actual |
| 3 | Analisis diagnostico | Que rarezas se asocian con precios mas altos? Que cartas aparecen en mas sets y que puede explicar su presencia? | `vw_fact_card_set_appearances`, `vw_dim_cards_descriptive`, `vw_dim_sets_descriptive`, `vw_dim_rarities_descriptive`, `vw_fact_card_prices_descriptive` | Foco actual |
| 4 | Historico / predictivo | Que correlaciones y tendencias aparecen entre snapshots? Que cartas muestran variaciones relevantes por marketplace? | `vw_fact_card_price_variation_predictive`, `vw_dim_snapshots_descriptive`, `vw_dim_marketplaces_descriptive`, `vw_dim_currencies_descriptive`, `vw_dim_cards_descriptive` | Foco actual |
| 5 | Analisis prescriptivo | Que cartas presentan senales para seguimiento prioritario? Que oportunidades requieren revision antes de convertirse en recomendacion? | `vw_fact_card_prices_descriptive`, `vw_fact_card_set_appearances`, `vw_fact_card_price_variation_predictive`, dimensiones relacionadas | Foco actual |
| 6 | Calidad de datos | Hay relaciones huerfanas, duplicados o baja cobertura? Que controles deben validarse antes de interpretar precios y rankings? | Todas las vistas de consumo acordadas | Pendiente tras paginas 1-5 |

## Organizacion de medidas

Las dimensiones se usan para filtrar, segmentar y agrupar. Las medidas deben declararse sobre hechos o en una tabla dedicada de medidas, manteniendo trazabilidad con la vista que alimenta el calculo.

```text
vw_fact_card_prices_descriptive              -> medidas de precio actual
vw_fact_card_set_appearances                 -> medidas de apariciones, sets, rarezas
vw_fact_card_price_variation_predictive      -> medidas historicas / variacion
Dimensiones vw_dim_*                         -> filtros, segmentadores, agrupaciones
```

## Registro de medidas

| Medida | Formula o descripcion | Tabla/consulta | Estado | Notas |
|---|---|---|---|---|
|  |  |  | Pendiente |  |
