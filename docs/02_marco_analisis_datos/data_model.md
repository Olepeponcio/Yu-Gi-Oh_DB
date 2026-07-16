# Modelo de datos — tablas madre

[Inicio](../../README.md) → [Marco de análisis](README.md) → Modelo de datos

Estado: punto de partida anterior al diseño de views.

## Principios

- Una tabla, una granularidad y una única verdad.
- PK y FK físicas antes del modelo semántico.
- Precio general de carta separado de precio de impresión.
- Moneda, marketplace y snapshot declarados en cada precio.
- Valor raw de rareza preservado; solo valores válidos entran en `rarity_types`.
- Ningún hecho se relaciona con otro hecho.

## Relaciones

```text
cards 1 -> * card_printings * <- 1 sets
rarity_types 1 -> * card_printings

cards 1 -> * card_price_history
marketplaces 1 -> * card_price_history
currencies 1 -> * card_price_history

cards 1 -> * card_images/card_typelines/card_linkmarkers
cards 1 -> 0..1 card_banlist
```

## Diccionario de tablas madre

### `cards`

- **Finalidad:** mantener la entidad principal y los atributos vigentes de cada carta.
- **Grano:** una fila por carta de YGOPRODeck.
- **Clave primaria:** `card_id`, identificador recibido de la API.
- **Relaciones:** lado 1 de `card_printings`, `card_price_history`, `card_images`, `card_banlist`, `card_typelines` y `card_linkmarkers`.
- **Datos almacenados:** nombre, tipos, textos, raza, arquetipo, URL, estadísticas de monstruo y marcas temporales de creación/actualización.
- **Criterio de actualización:** `INSERT ... ON DUPLICATE KEY UPDATE`; cada carga actualiza los atributos conocidos sin cambiar `card_id`.
- **Uso analítico:** dimensión base para describir, agrupar y filtrar cualquier hecho asociado a una carta.
- **Limitaciones:** representa el estado vigente, no el historial de cambios de texto o estadísticas; muchos atributos solo aplican a determinados tipos de carta.

### `sets`

- **Finalidad:** catalogar los sets o colecciones en los que aparecen cartas.
- **Grano:** una fila por nombre único de set.
- **Clave primaria:** `set_id`, identificador interno autoincremental; `set_name` es clave natural única.
- **Relaciones:** lado 1 de `card_printings` mediante `set_id`.
- **Datos almacenados:** nombre del set y marcas temporales de creación/actualización.
- **Criterio de actualización:** inserción idempotente por `set_name`; los sets ya existentes se reutilizan.
- **Uso analítico:** dimensión para agrupar impresiones, contar cartas y analizar `set_price_usd` por colección.
- **Limitaciones:** no contiene fecha de lanzamiento, región ni metadatos editoriales; un cambio textual del nombre podría crear otra entidad.

### `rarity_types`

- **Finalidad:** catalogar rarezas semánticas válidas separándolas del valor raw recibido.
- **Grano:** una fila por combinación `rarity_name` + `rarity_code`.
- **Clave primaria:** `rarity_id`, identificador interno autoincremental; la combinación nombre/código es única.
- **Relaciones:** lado 1 opcional de `card_printings`; una impresión inválida puede tener `rarity_id = NULL`.
- **Datos almacenados:** nombre y código normalizados de rareza, más marcas temporales.
- **Criterio de actualización:** inserción idempotente; solo las rarezas clasificadas como válidas o normalizadas entran en el catálogo.
- **Uso analítico:** dimensión para filtrar y comparar impresiones por rareza válida.
- **Limitaciones:** no representa etiquetas internas, valores numéricos anómalos ni ausencias; esos casos se conservan únicamente en los campos raw de `card_printings`.

### `card_printings`

- **Finalidad:** representar cada aparición o impresión de una carta dentro de un set y conservar la calidad de su rareza fuente.
- **Grano:** carta + `set_code` + nombre raw de rareza + código raw de rareza.
- **Clave primaria:** `printing_id`; existe una restricción única sobre el grano declarado.
- **Relaciones:** muchas impresiones pertenecen a una `card`, un `set` y, cuando es válida, una `rarity_type`.
- **Datos almacenados:** códigos de impresión, rareza raw y normalizada, calidad de fuente y `set_price_usd`.
- **Criterio de actualización:** se eliminan las filas de las cartas incluidas en la carga y se insertan de nuevo desde el payload actual.
- **Uso analítico:** hecho base para apariciones, reimpresiones, cobertura de rareza y precio actual atribuible a set/rareza.
- **Limitaciones:** `set_price_usd` no es histórico y puede ser nulo; no debe mezclarse con el precio general de `card_price_history`; `rarity_id` nulo no implica que falte el literal raw.

### `marketplaces`

- **Finalidad:** mantener el catálogo controlado de mercados de los precios generales.
- **Grano:** una fila por marketplace.
- **Clave primaria:** `marketplace_id`; `marketplace_code` también es único.
- **Relaciones:** lado 1 de `card_price_history`.
- **Datos almacenados:** código estable, nombre visible y región de mercado.
- **Criterio de actualización:** catálogo sembrado por `schema.sql` mediante upsert; no se carga desde el payload ETL.
- **Uso analítico:** dimensión para segmentar y comparar precios entre fuentes comerciales.
- **Limitaciones:** región es descriptiva y no garantiza disponibilidad real; añadir una fuente requiere cambiar el esquema y el mapeo del transformador.

### `currencies`

- **Finalidad:** declarar explícitamente la moneda de cada observación de precio.
- **Grano:** una fila por moneda admitida.
- **Clave primaria:** `currency_code`, código de tres caracteres.
- **Relaciones:** lado 1 de `card_price_history`.
- **Datos almacenados:** código y nombre visible de moneda.
- **Criterio de actualización:** catálogo sembrado por `schema.sql` mediante upsert; actualmente contiene EUR y USD.
- **Uso analítico:** dimensión obligatoria para filtrar precios y evitar agregaciones entre monedas incompatibles.
- **Limitaciones:** el catálogo no contiene símbolos, decimales ni histórico de tipos de cambio; la conversión concreta vive en cada observación convertida.

### `card_price_history`

- **Finalidad:** conservar observaciones históricas de precio general por carta, mercado y moneda.
- **Grano:** carta + marketplace + moneda + `snapshot_at`.
- **Clave primaria:** `price_history_id`; el grano declarado tiene además una restricción única.
- **Relaciones:** muchas observaciones pertenecen a una `card`, un `marketplace` y una `currency`.
- **Datos almacenados:** fecha del snapshot, precio no negativo, origen (`api` o `currency_conversion`) y tipo de cambio cuando corresponde.
- **Criterio de actualización:** append-only entre ejecuciones; una colisión exacta del mismo grano actualiza precio y metadatos. Se respalda y restaura durante el reset.
- **Uso analítico:** precio vigente mediante el último snapshot y series temporales para variaciones o tendencias.
- **Limitaciones:** no tiene set ni rareza porque la API no ofrece ese precio a nivel de impresión; no se deben sumar o promediar EUR y USD sin conversión explícita.

### `card_images`

- **Finalidad:** registrar las imágenes publicadas para cada carta.
- **Grano:** una fila por imagen de YGOPRODeck.
- **Clave primaria:** `image_id`, identificador recibido de la API.
- **Relaciones:** muchas imágenes pertenecen a una `card`; se eliminan en cascada si desaparece la carta.
- **Datos almacenados:** URL original, pequeña y recortada.
- **Criterio de actualización:** reemplazo completo por carta en cada carga; después se insertan las imágenes actuales.
- **Uso analítico:** soporte visual en informes, fichas y exploración de cartas; no es una tabla de medidas.
- **Limitaciones:** almacena enlaces, no archivos ni disponibilidad histórica; una carta puede tener varias imágenes y eso multiplica filas al unirla directamente.

### `card_banlist`

- **Finalidad:** conservar el estado vigente de restricciones competitivas informado para cada carta.
- **Grano:** cero o una fila por carta.
- **Clave primaria:** `card_id`, que también es FK a `cards`.
- **Relaciones:** relación 1 a 0..1 con `cards`; eliminación en cascada.
- **Datos almacenados:** estados de banlist para TCG, OCG y GOAT.
- **Criterio de actualización:** reemplazo completo por carta en cada carga; solo se inserta cuando la API aporta banlist.
- **Uso analítico:** segmentar cartas por formato y estado de restricción vigente.
- **Limitaciones:** no conserva fechas ni historial de cambios; un nulo significa ausencia de dato, no necesariamente carta permitida.

### `card_typelines`

- **Finalidad:** normalizar la lista ordenada de tipos o clasificaciones de una carta.
- **Grano:** una tipología dentro de una carta.
- **Clave primaria:** compuesta por `card_id` + `typeline`.
- **Relaciones:** muchas typelines pertenecen a una `card`; eliminación en cascada.
- **Datos almacenados:** literal de tipología y su posición original.
- **Criterio de actualización:** reemplazo completo por carta en cada carga.
- **Uso analítico:** relación puente para filtrar cartas por múltiples tipos sin almacenar listas en una columna.
- **Limitaciones:** `position` conserva orden pero no forma parte de la PK; unir esta tabla puede multiplicar una carta por su número de typelines.

### `card_linkmarkers`

- **Finalidad:** normalizar los marcadores direccionales de las cartas Link.
- **Grano:** un marcador dentro de una carta.
- **Clave primaria:** compuesta por `card_id` + `linkmarker`.
- **Relaciones:** muchos marcadores pertenecen a una `card`; eliminación en cascada.
- **Datos almacenados:** literal del marcador y su posición original.
- **Criterio de actualización:** reemplazo completo por carta en cada carga.
- **Uso analítico:** describir y filtrar cartas Link por dirección o combinación de marcadores.
- **Limitaciones:** solo aplica a cartas Link; unirla directamente multiplica una carta por marcador y `position` no forma parte de la PK.

## Siguiente hito

Usar el [registro modular de views](view_design/README.md). La primera rama es descriptive; diagnostic, predictive y prescriptive solo avanzan cuando sus dependencias anteriores están validadas.
