# Informe de conclusiones descriptivo y diagnostico

Fuente de evidencias: exportaciones CSV de `powerbi/exportaciones/analisis_desc_diag`.

Fecha de elaboracion: 2026-06-23.

## 1. Objetivo

Convertir los visuales descriptivos y diagnosticos de Power BI en conclusiones reutilizables para orientar decisiones comerciales sobre cartas individuales de Yu-Gi-Oh.

El informe sigue la regla del marco:

```text
hallazgo -> por que importa -> accion sugerida
```

## 2. Alcance y cautelas

- El analisis trabaja con precios observados en el mercado secundario.
- Los precios exportados por marketplace corresponden a `ebay`, `amazon`, `coolstuffinc` y `tcgplayer`.
- No se mezclan monedas en una misma conclusion sin segmentacion visible.
- Los outliers deben revisarse antes de convertir rankings en recomendaciones.
- El interes estimado por arquetipo es un proxy: combina presencia, impresiones y valor observado; no equivale a ventas reales.

## 3. Conclusiones descriptivas

### 3.1 Precio medio por marketplace

Evidencia principal:

| Marketplace | Precio medio |
|---|---:|
| ebay | $4,56 |
| amazon | $4,28 |
| coolstuffinc | $1,45 |
| tcgplayer | $1,19 |

Conclusion:

`ebay` y `amazon` muestran precios medios superiores a `tcgplayer` y `coolstuffinc`. La comparacion entre marketplaces debe mantenerse separada, porque cada fuente puede representar condiciones de mercado distintas.

Accion sugerida:

Usar marketplace como segmentador obligatorio en visuales monetarios y evitar un ranking unico de precios si no se explica la fuente.

### 3.2 Cartas con mayor precio medio

Evidencia principal:

| Carta | Precio medio |
|---|---:|
| Blood Mefist | $933,73 |
| Ten Thousand Dragon | $679,22 |
| Holactie the Creator of Light | $506,43 |
| Doriado | $501,51 |
| Get Your Game On! | $456,75 |

Conclusion:

El ranking de precio medio identifica cartas de alto valor, pero no debe interpretarse automaticamente como recomendacion comercial. Algunas cartas pueden deber su posicion a rareza, disponibilidad limitada o registros extremos.

Accion sugerida:

Usar este ranking como entrada de revision, cruzandolo con rareza, set, outliers y legalidad antes de destacar cartas.

### 3.3 Cartas con mayor presencia en sets

Evidencia principal:

| Carta | Sets |
|---|---:|
| Mystical Space Typhoon | 58 |
| Blue-Eyes White Dragon | 56 |
| Call of the Haunted | 50 |
| Dark Magician | 45 |
| Book of Moon | 37 |

Conclusion:

Las cartas con mas apariciones en sets muestran alta recurrencia y disponibilidad historica. Esta presencia no implica mayor valor por si sola, pero si indica cartas reconocibles y utiles para segmentar analisis posteriores.

Accion sugerida:

Usar estas cartas como candidatas de seguimiento cuando tambien cumplan precio relevante, legalidad competitiva o relacion con arquetipos prioritarios.

### 3.4 Sets con mayor valor de mercado

Evidencia principal:

| Set | Valor observado |
|---|---:|
| Shonen Jump Championship 2007 Prize Card A | 115033.33 |
| Shonen Jump Championship 2005 Prize Card | 95074.95 |
| Yu-Gi-Oh! Championship Series 2010 Prize Cards | 30547.47 |
| Retro Pack | 25119.51 |
| Shonen Jump Championship 2004 Prize Card | 24067.80 |

Conclusion:

Los sets con mayor valor estan muy influidos por cartas premio o productos con disponibilidad excepcional. Estos sets explican valor extremo, pero pueden distorsionar una lectura general del catalogo.

Accion sugerida:

Separar sets de premio o ediciones excepcionales de los analisis de producto comun antes de proponer decisiones comerciales.

## 4. Conclusiones diagnosticas

### 4.1 Rarezas asociadas a precios superiores

Evidencia principal:

| Rareza | Precio medio rareza | Precio medio global | Elevacion |
|---|---:|---:|---:|
| 10000 Secret Rare | 1961.53 | 46.00 | 1915.53 |
| Starlight Rare | 416.48 | 46.00 | 370.48 |
| Ghost Rare | 318.17 | 46.00 | 272.16 |
| Duel Terminal Rare Parallel Rare | 301.75 | 46.00 | 255.75 |
| Extra Secret Rare | 262.63 | 46.00 | 216.63 |

Conclusion:

La rareza es un factor explicativo fuerte del precio. `10000 Secret Rare`, `Starlight Rare` y `Ghost Rare` quedan claramente por encima del precio medio global.

Accion sugerida:

Usar rareza como criterio de justificacion comercial, pero comprobar outliers cuando el precio maximo de una rareza sea excepcional.

### 4.2 Outliers de precio

Evidencia principal:

| Carta | Rareza | Precio maximo |
|---|---|---:|
| Crush Card Virus | Ultra Rare | 115033.33 |
| Des Volstgalph | Ultra Rare | 95074.95 |
| Cyber-Stein | Ultra Rare | 24067.80 |
| Gold Sarcophagus | Ultra Rare | 24000.00 |
| Darklord Asmodeus | Ultra Rare | 20299.50 |

Conclusion:

Los outliers se concentran en impresiones muy concretas, especialmente cartas premio o ediciones excepcionales. Estos valores pueden elevar medias por rareza, set o arquetipo.

Accion sugerida:

Marcar estas cartas como `Revisar antes de accionar` y excluirlas o segmentarlas cuando el objetivo sea entender precios representativos.

### 4.3 Arquetipos con mayor interes estimado

Evidencia principal:

| Arquetipo | Peso estimado | Cartas | Impresiones | Codigos set |
|---|---:|---:|---:|---:|
| Darklord | 30662.86 | 30 | 84 | 72 |
| Blue-Eyes | 10511.25 | 40 | 326 | 274 |
| Lightsworn | 9715.02 | 43 | 187 | 157 |
| Utopia | 8079.59 | 41 | 117 | 95 |
| Harpie | 6822.49 | 33 | 196 | 176 |

Conclusion:

`Darklord` lidera por peso estimado, pero su lectura debe revisarse porque incluye precios maximos muy altos. `Blue-Eyes`, `Lightsworn`, `Utopia` y `Harpie` combinan volumen de cartas, impresiones y presencia amplia.

Accion sugerida:

Usar estos arquetipos como filtros prioritarios para buscar cartas destacables, manteniendo control de outliers.

### 4.4 Cartas candidatas competitivas

Evidencia principal:

| Carta | Impresiones | Codigos set | Precio medio set | Precio maximo set | Estado TCG |
|---|---:|---:|---:|---:|---|
| Blue-Eyes White Dragon | 77 | 68 | 114.49 | 2999.98 | unlimited |
| Red-Eyes Black Dragon | 39 | 34 | 72.46 | 920.45 | unlimited |
| Dark Magician | 59 | 53 | 52.29 | 797.61 | unlimited |
| Dark Magician Girl | 43 | 38 | 21.79 | 530.15 | unlimited |
| Book of Moon | 46 | 37 | 10.01 | 436.13 | unlimited |

Conclusion:

Las candidatas competitivas combinan legalidad TCG, varias impresiones y precio medio relevante. `Blue-Eyes White Dragon`, `Dark Magician` y `Book of Moon` destacan por presencia y reconocimiento, aunque por motivos comerciales distintos.

Accion sugerida:

Pasar estas cartas al bloque prescriptivo como candidatas, no como recomendaciones finales. Deben clasificarse segun funcion: carta principal potencial, carta complementaria o carta destacada.

## 5. Riesgos de interpretacion

- Un precio alto puede depender de una unica impresion.
- Una carta con muchas apariciones en sets puede ser muy disponible y no necesariamente cara.
- Un arquetipo con peso estimado alto puede estar inflado por una carta extrema.
- Los rankings de precio no sustituyen la revision de legalidad, rareza y set.
- Los precios historicos solo deben usarse como tendencia si existen suficientes snapshots de ETL.

## 6. Acciones comerciales sugeridas

1. Priorizar cartas candidatas competitivas no afectadas por outliers.
2. Usar `Blue-Eyes`, `Dark Magician`, `Lightsworn`, `Utopia` y `Harpie` como arquetipos de exploracion comercial.
3. Separar cartas premio y precios extremos antes de calcular conclusiones generales.
4. Mantener marketplace como segmentador en visuales de precio.
5. Crear reglas prescriptivas para clasificar cartas en:

```text
carta principal potencial
carta complementaria
carta destacada comercial
revisar antes de accionar
```

## 7. Cierre

El analisis descriptivo permite entender catalogo, precios, marketplaces, sets y presencia de cartas. El diagnostico explica por que ciertos valores destacan y donde existen riesgos de interpretacion.

La conclusion operativa es pasar al bloque prescriptivo con una condicion: ninguna recomendacion debe salir solo de un ranking. Debe combinar valor, contexto, calidad del dato y legalidad.
