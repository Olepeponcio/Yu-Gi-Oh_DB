# Proceso de trabajo en Power BI

Power BI se conectara a MySQL:

```text
yugioh_db
```

La conexion no debe alterar las tablas madre. El informe debe cargarse desde las vistas `vw_` del modelo relacional simplificado.

## Fondo de pagina inicial

Para la primera pagina de navegacion/cuadro de control:

```text
docs/03_powerbi/assets/fondo_control_powerbi_fondo2.png
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

| Pagina | Pregunta base | Vistas base |
|---|---|---|
| Vista general | Que contiene el catalogo y que fuentes de precio existen | `vw_dim_cards_descriptive`, `vw_dim_marketplaces_descriptive` |
| Precios actuales | Como se distribuyen los precios por marketplace y moneda | `vw_fact_card_prices_descriptive` |
| Sets y rarezas | Que sets, apariciones y rarezas explican diferencias | `vw_fact_card_set_appearances`, `vw_dim_sets_descriptive`, `vw_dim_rarities_descriptive` |
| Historico de precios | Existe variacion temporal comparable | `vw_fact_card_price_variation_predictive`, `vw_dim_snapshots_descriptive` |

## Registro de medidas

| Medida | Formula o descripcion | Tabla/consulta | Estado | Notas |
|---|---|---|---|---|
|  |  |  | Pendiente |  |
