# Marco de analisis de datos

Este directorio documenta el proceso para poner en practica el analisis de datos del proyecto SQL DB Yu-Gi-Oh.

La finalidad es usar el proyecto como aprendizaje y portfolio: partir de una decision analitica, preparar datos con Python y MySQL, analizar con SQL y dejar Power BI para una fase posterior.

## Flujo practico del analisis

```text
decision -> preguntas -> datos -> fuentes -> preparacion -> analisis -> comunicacion
```

## Paso 1: formular la decision

El analisis debe empezar por una decision, no por una tabla.

Decision marco del proyecto:

> Identificar que cartas, rarezas, sets y precios del mercado secundario pueden orientar decisiones sobre productos comerciales de Yu-Gi-Oh.

La decision parte de una segmentacion de mercado:

- Mercado secundario de cartas individuales: precios observados en marketplaces.
- Mercado oficial TCG occidental: producto sellado publicado por Konami para America, Europa y otros territorios occidentales.

Alcance operativo actual:

- El proyecto analiza el mercado secundario.
- El mercado oficial queda como contexto de referencia, no como capa ETL obligatoria.
- No se cargan todavia productos sellados ni MSRP oficial en MySQL.

Decision de alcance:

> Si. Podemos prescindir de una ETL del mercado oficial para esta fase.

Motivo:

- El objetivo actual se sostiene con datos de cartas, rarezas, sets y precios de mercado secundario.
- El MSRP oficial corresponde a producto sellado, no a precio individual de carta.
- Power BI puede comunicar decisiones sobre valor relativo, rareza, set y marketplace sin integrar aun MSRP.
- El MSRP oficial puede incorporarse despues como benchmark para comparar producto sellado frente a valor estimado de cartas.

Ejemplos de decisiones derivadas:

- Que cartas destacar en un dashboard comercial.
- Que sets concentran mayor valor de mercado.
- Que rarezas elevan el precio medio.
- Que cartas pueden funcionar como cartas principales de un pack.
- Que cartas baratas pueden complementar productos de mayor valor.

## Paso 2: transformar la decision en preguntas analiticas

Las preguntas convierten la decision en trabajo medible.

Preguntas iniciales:

- 1. Que cartas tienen mayor precio medio por marketplace?
  - `sql/analysis/views/vw_fact_card_prices.sql`

- 2. Que rarezas se asocian con precios mas altos?
  - `sql/analysis/views/diagnostic/vw_diag_price_by_rarity.sql`

- 3. Que sets acumulan mas valor potencial?

- 4. Que tipos de carta dominan el catalogo?

- 5. Que cartas aparecen en mas sets?

- 6. Que cartas muestran variacion de precio entre ejecuciones del ETL?
  - `sql/analysis/queries/diagnostic/q_diag_price_variation_usd.sql`
  - `sql/analysis/queries/diagnostic/q_diag_relevant_price_increases.sql`

- 7. Que diferencias existen entre precios de Cardmarket, TCGPlayer, eBay, Amazon y CoolStuffInc?

## Paso 3: identificar datos necesarios

Datos necesarios para responder las preguntas:

- Datos base de carta: nombre, tipo, atributo, nivel, ataque, defensa, arquetipo.
- Apariciones en sets: set, codigo, rareza y precio declarado del set.
- Precios por marketplace.
- Historico de precios por ejecucion del ETL.
- Restricciones de banlist.
- Imagenes y enlaces para soporte visual en Power BI.

Segmentacion de precios:

- `cardmarket_price`: precio de Cardmarket en EUR.
- `tcgplayer_price`: precio de TCGPlayer en USD.
- `ebay_price`: precio de eBay en USD.
- `amazon_price`: precio de Amazon en USD.
- `coolstuffinc_price`: precio de CoolStuffInc en USD.
- `set_price`: precio asociado al set en USD segun la API de YGOPRODeck.

Por tanto, los datos obtenidos no son todos en USD:

- Europa/Cardmarket usa EUR.
- TCGPlayer, eBay, Amazon, CoolStuffInc y `set_price` usan USD.
- Cualquier comparativa monetaria agregada debe separar moneda o aplicar conversion antes de mezclar mercados.

Tipos de datos utilizados:

- Estructurados: tablas MySQL normalizadas, views SQL y CSV analiticos.
- Semi-estructurados: JSON descargado desde la API de YGOPRODeck.
- No estructurados: imagenes de cartas, descripciones textuales y enlaces externos usados como apoyo visual o contextual.

Documentos relacionados:

- [Analisis JSON API](api_json_analysis.md)
- [Modelo de datos](data_model.md)

## Paso 4: localizar sistemas fuente

Fuente principal:

- API publica de YGOPRODeck.

Fuentes oficiales de contexto:

- Konami North America publica fichas de producto TCG con `MSRP` en USD, por ejemplo boosters con MSRP por pack.
- Konami Europe mantiene catalogo oficial de productos TCG para Europa y territorios distribuidos desde Europa, pero las paginas revisadas no muestran un MSRP equivalente como campo estructurado.

Estructura oficial de precios:

- El MSRP oficial se publica a nivel de producto sellado: booster pack, structure deck, tin u otros productos.
- El MSRP no define el valor individual de una carta.
- El MSRP sirve para comparar precio recomendado de producto sellado frente a valor secundario estimado, pero requiere otra capa de datos.

Decision tecnica:

- No implementar ahora ETL de producto sellado oficial.
- Mantener el modelo actual centrado en cartas y mercado secundario.
- Registrar el MSRP oficial como posible escalada futura si el proyecto pasa de analisis de cartas a analisis de rentabilidad de producto sellado.

Sistemas internos del proyecto:

- Python ETL para extraer, transformar y cargar datos.
- `data/raw/cardinfo_latest.json` como copia raw de la ultima descarga.
- MySQL como base relacional de analisis.
- `sql/analysis/` como capa SQL analitica.
- Power BI como capa de comunicacion.

## Paso 5: preparar los datos

La preparacion ocurre principalmente en Python y MySQL.

Tareas clave:

- Extraer datos desde la API.
- Guardar copia raw para trazabilidad.
- Normalizar objetos anidados en tablas relacionales.
- Convertir precios a valores numericos.
- Separar dimensiones como sets y rarezas.
- Cargar tablas base de forma idempotente.
- Insertar historico de precios por ejecucion real del ETL.
- Validar relaciones entre cartas, sets, rarezas, precios e imagenes.

Resultado esperado:

```text
API YGOPRODeck -> Python ETL -> MySQL -> SQL views semanticas
```

## Paso 6: analizar

El analisis se ejecuta principalmente con SQL sobre MySQL.

Niveles de analisis aplicables:

- Descriptivo: que cartas, sets, tipos, rarezas y precios existen.
- Diagnostico: que variables explican diferencias de precio entre cartas, rarezas, sets y marketplaces.
- Predictivo: queda preparado tecnicamente, pero depende de acumular historico suficiente mediante cargas diarias del ETL.
- Prescriptivo: se abordara despues, cuando exista base temporal suficiente para sostener recomendaciones por tendencia.

Alcance actual:

> El trabajo principal se centra en analisis descriptivo y diagnostico. La base predictiva se alimentara progresivamente con una carga diaria del ETL.

Metodo de trabajo por pregunta:

```text
decision -> pregunta -> variable objetivo -> variables explicativas -> consulta/view -> tipo de analisis
```

Este metodo obliga a conectar cada consulta con una decision concreta antes de convertirla en resultado analitico. La consulta o view no debe existir solo porque la tabla lo permite, sino porque responde a una pregunta medible.

Nota sobre historico:

> El historico de precios utilizado no procede de una serie historica externa, sino de snapshots capturados por nuestra ETL. Por tanto, las conclusiones temporales solo son validas para el intervalo registrado en `card_price_history`.

Artefactos previstos:

- Consultas exploratorias.
- Views SQL semanticas: `vw_dim_*`, `vw_fact_*`, `vw_bridge_*`, `vw_agg_*`, `vw_desc_*`.
- Views SQL diagnosticas fuera del modelo: `views/diagnostic/vw_diag_*`.
- Tablas resumen por carta, set, rareza y marketplace.
- Medidas de evolucion cuando haya historico suficiente.

## Convencion de views analiticas

| Nombre de view | Referencia a problemas que buscamos resolver |
|---|---|
| `vw_dim_card` | Centralizar la descripcion de cada carta y evitar repetir joins basicos. |
| `vw_dim_set` | Analizar expansiones, productos y presencia de cartas por set. |
| `vw_dim_rarity` | Comparar el impacto de la rareza sobre precios y disponibilidad. |
| `vw_ref_banlist_status` | Normalizar estados competitivos para filtros consistentes. |
| `vw_bridge_card_set` | Resolver la relacion carta-set-rareza-codigo de impresion. |
| `vw_fact_card_prices` | Medir precios actuales por carta y marketplace sin mezclar monedas sin control. |
| `vw_fact_price_history` | Analizar variaciones entre ejecuciones del ETL. |
| `vw_agg_card_price_current` | Preparar precio actual resumido por carta para dashboards. |
| `vw_agg_set_value` | Estimar que sets concentran mayor valor potencial. |
| `vw_diag_cards_without_price` | Localizar cartas sin precios para revisar calidad de datos. |
| `vw_diag_price_by_rarity` | Diagnosticar si la rareza explica diferencias de precio. |
| `vw_diag_price_outliers` | Detectar precios extremos antes de usarlos como conclusion. |

## Paso 7: comunicar

La comunicacion mediante Power BI queda pausada hasta consolidar la capa SQL en MySQL.

Cada resultado debe responder:

1. Que se ha encontrado.
2. Por que importa.
3. Que accion o decision sugiere.

Salidas esperadas:

- Dashboard de vision general del catalogo.
- Ranking de cartas por precio y rareza.
- Analisis de sets con mayor valor potencial.
- Comparativa de marketplaces.
- Evolucion de precios cuando exista historico suficiente.
- Conclusiones orientadas a portfolio: problema, metodo, hallazgos y recomendacion.

## Documentos del marco

- [Analisis JSON API](api_json_analysis.md)
- [Modelo de datos](data_model.md)
- [Modelo relacional](relational_model.svg)
- [Infografia de views SQL](infografia_views_sql.svg)

## Fuentes de referencia

- [YGOPRODeck API Guide](https://ygoprodeck.com/api-guide/): documenta monedas de `card_prices` y `set_price`.
- [Konami North America - Blazing Dominion](https://www.yugioh-card.com/en/products/blzd/): ejemplo oficial de producto TCG con MSRP en USD.
- [Konami Europe - Products](https://www.yugioh-card.com/eu/products/): catalogo oficial europeo de productos TCG.
- [Konami Europe - Magnificent Monsters](https://www.yugioh-card.com/eu/product/magnificent-monsters/): ejemplo de distribucion occidental diferenciada entre Americas y mercados distribuidos desde Europa.
