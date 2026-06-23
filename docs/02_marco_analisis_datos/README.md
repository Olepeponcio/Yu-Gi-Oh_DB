# Marco de analisis de datos

Este README es la fuente canonica del analisis de datos del proyecto SQL DB Yu-Gi-Oh.

Finalidad: convertir datos de cartas, sets, rarezas, precios y legalidad en acciones comerciales reutilizables para Power BI.

Los README de `sql/analysis/` y `powerbi/` solo documentan implementacion. No deben redefinir preguntas, decisiones ni avances del marco.

## Decision marco

> Identificar que cartas, rarezas, sets y precios del mercado secundario pueden orientar decisiones sobre productos comerciales de Yu-Gi-Oh.

Alcance actual:

- Mercado analizado: mercado secundario de cartas individuales.
- Fuente principal: API publica de YGOPRODeck.
- Capa de datos: Python ETL -> MySQL -> SQL views -> Power BI.
- Mercado oficial TCG y MSRP: contexto futuro, no ETL obligatoria en esta fase.

Motivo:

- El objetivo actual se sostiene con precios observados por carta, set, rareza y marketplace.
- El MSRP oficial aplica a producto sellado, no al precio individual de carta.
- Power BI puede comunicar acciones sobre valor relativo, agrupacion y priorizacion sin integrar aun producto sellado.

## Flujo de trabajo

```text
decision -> pregunta -> datos -> preparacion -> analisis -> accion comercial -> comunicacion
```

Regla:

> Cada visual comercial debe terminar en una accion sugerida, no solo en una tabla o ranking.

## Avances registrados

| Bloque | Estado | Evidencia actual | Siguiente paso |
|---|---|---|---|
| Ingesta | Activo | ETL API/raw file, carga MySQL e historico en `card_price_history`. | Mantener ejecuciones periodicas para ampliar historico. |
| Modelo SQL | Activo | Tablas base y views `vw_dim_*`, `vw_bridge_*`, `vw_fact_*`, `vw_ref_*`, `vw_diag_*`. | Crear solo nuevas views cuando respondan a una accion comercial. |
| Power BI | Activo | Modelo consume views de MySQL en modo Importar. | Organizar paginas por bloque analitico y accion sugerida. |
| Prescriptivo | En curso | Query `sql/analysis/queries/card_comercial_actions.sql` y view `vw_diag_competitive_staple_candidates`. | Consolidar reglas de clasificacion comercial en view o medida estable. |

## Bloque descriptivo

Objetivo: saber que existe y como se distribuye.

Preguntas:

- Que cartas, tipos, sets y rarezas existen?
- Que cartas tienen mayor precio medio por marketplace?
- Que sets tienen mas cartas o impresiones?
- Como se distribuyen los precios por marketplace?

Artefactos:

- `vw_dim_card`
- `vw_dim_set`
- `vw_dim_rarity`
- `vw_dim_card_image`
- `vw_dim_card_typelines`
- `vw_fact_card_prices`
- `vw_bridge_card_set`
- `queries/descriptive/q_desc_*`

Uso comercial:

- Crear vision general del catalogo.
- Localizar cartas visibles para ranking inicial.
- Separar mercados por moneda antes de comparar.

## Bloque diagnostico

Objetivo: explicar diferencias, relaciones y riesgos de interpretacion.

Preguntas:

- Que rarezas se asocian con precios mas altos?
- Que cartas aparecen en mas sets?
- Que arquetipos concentran mas interes estimado?
- Que precios son outliers y deben revisarse antes de concluir?
- Que cartas candidatas combinan precio, reimpresiones y legalidad competitiva?

Artefactos:

- `vw_diag_price_by_rarity`
- `vw_diag_price_outliers`
- `vw_diag_high_demand_archetypes`
- `vw_diag_competitive_staple_candidates`
- `vw_bridge_card_banlist`
- `vw_ref_banlist_status`
- `queries/diagnostic/q_diag_*`

Uso comercial:

- Justificar por que una carta, rareza o set merece atencion.
- Evitar recomendaciones basadas en datos extremos o incompletos.
- Segmentar cartas por contexto competitivo.

## Bloque predictivo

Objetivo: preparar tendencia temporal, no prometer prediccion sin historico suficiente.

Preguntas:

- Que cartas muestran variacion de precio entre ejecuciones del ETL?
- Que cartas suben o bajan de forma relevante en los snapshots disponibles?
- Hay suficiente historial para hablar de tendencia?

Artefactos:

- `vw_fact_price_history`
- `queries/descriptive/q_desc_price_history_snapshots.sql`
- `queries/diagnostic/q_diag_price_variation_usd.sql`
- `queries/diagnostic/q_diag_relevant_price_increases.sql`

Criterio:

> El historico procede de snapshots de nuestra ETL, no de una serie historica externa. Las conclusiones temporales solo son validas para el intervalo registrado.

Uso comercial:

- Priorizar seguimiento de cartas con cambios relevantes.
- Evitar usar tendencia cuando solo haya pocos snapshots.
- Preparar alertas futuras de subida, bajada o volatilidad.

## Bloque prescriptivo

Objetivo: convertir hallazgos en acciones comerciales.

Acciones previstas:

| Accion comercial | Criterio medible | Salida esperada |
|---|---|---|
| Seleccionar carta principal de pack | Precio alto, rareza relevante, presencia en set, legalidad o tendencia positiva. | `Carta principal potencial` |
| Seleccionar carta complementaria barata | Precio bajo, relacion tematica, disponibilidad o presencia en set. | `Carta complementaria` |
| Destacar carta en dashboard comercial | Precio, rareza, marketplace, set, arquetipo, outlier controlado o variacion historica. | `Carta destacada comercial` |
| Revisar calidad antes de recomendar | Precio extremo, moneda mezclada, falta de precio o relacion incompleta. | `Revisar antes de accionar` |

Metodo:

```text
pregunta comercial -> criterio medible -> SQL/medida -> clasificacion -> visual -> accion
```

Criterios iniciales:

- Valor: precio medio, precio maximo, ranking o valor acumulado por set.
- Contexto: set, rareza, marketplace, arquetipo y banlist.
- Calidad: excluir outliers, precios sin moneda comparable y datos incompletos.
- Uso: diferenciar carta gancho, carta de apoyo y carta destacable.

Artefactos actuales:

- `sql/analysis/queries/card_comercial_actions.sql`
- `vw_diag_competitive_staple_candidates`
- `vw_diag_price_outliers`
- `vw_diag_high_demand_archetypes`
- Medidas Power BI sobre `vw_fact_card_prices` y `vw_fact_price_history`.

Siguiente consolidacion:

- Convertir reglas prescriptivas estables en una view versionada si se usan de forma recurrente.
- Mantener reglas experimentales como query hasta validarlas.
- Documentar en Power BI el motivo de seleccion de cada carta destacada.

## Datos necesarios

- Carta: nombre, tipo, atributo, nivel, ataque, defensa, arquetipo.
- Set: expansion, codigo, rareza, precio declarado del set.
- Precio: marketplace, moneda, valor actual.
- Historico: snapshots por ejecucion real del ETL.
- Legalidad: formato y estado de banlist.
- Imagenes: apoyo visual para Power BI.

Monedas:

- `cardmarket_price`: EUR.
- `tcgplayer_price`, `ebay_price`, `amazon_price`, `coolstuffinc_price`, `set_price`: USD.

Regla:

> No mezclar monedas en una misma conclusion sin conversion explicita o segmentacion visible.

## Comunicacion en Power BI

Cada pagina debe responder:

1. Que se ha encontrado.
2. Por que importa.
3. Que accion sugiere.

Bloques recomendados:

- Catalogo y cobertura.
- Precio actual por carta y marketplace.
- Rareza, set y arquetipo.
- Calidad y outliers.
- Candidatas comerciales.
- Evolucion temporal cuando haya historico suficiente.

## Documentos del marco

- [Analisis JSON API](api_json_analysis.md)
- [Modelo de datos](data_model.md)
- [Datos sensibles y calidad](privacidad_calidad_datos_modelo.md)
- [Modelo relacional](relational_model.svg)
- [Infografia de views SQL](infografia_views_sql.svg)

## Fuentes de referencia

- [YGOPRODeck API Guide](https://ygoprodeck.com/api-guide/)
- [Konami North America - Blazing Dominion](https://www.yugioh-card.com/en/products/blzd/)
- [Konami Europe - Products](https://www.yugioh-card.com/eu/products/)
