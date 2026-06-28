# Datos sensibles y calidad de los datos

## 1. Objetivo del documento

Este documento analiza las implicaciones de privacidad y calidad de datos del modelo relacional del proyecto SQL DB Yu-Gi-Oh.

El proyecto trabaja con datos de cartas, sets, rarezas, precios, imagenes y restricciones obtenidas desde la API publica de YGOPRODeck. Su finalidad es analitica y formativa: preparar datos para SQL, MySQL y Power BI.

## 2. Naturaleza de los datos

El modelo no trabaja con datos personales de usuarios, compradores, vendedores o jugadores concretos.

Las entidades principales son:

- Cartas.
- Sets.
- Rarezas.
- Imagenes.
- Precios por marketplace.
- Historico de precios.
- Restricciones de banlist.
- Tipologias y marcadores Link.

Por tanto, el riesgo de privacidad directa es bajo.

Sin embargo, siguen existiendo cuestiones relevantes:

- Uso correcto de datos procedentes de una API externa.
- Respeto a URLs, imagenes y contenido publicado por terceros.
- Interpretacion responsable de precios de mercado.
- Control de calidad antes de tomar decisiones comerciales.

## 3. Datos potencialmente sensibles

Aunque no hay datos personales, algunos elementos requieren cuidado.

| Dato | Sensibilidad | Motivo |
|---|---|---|
| `ygoprodeck_url` | Baja | Es una URL publica, pero depende de una fuente externa |
| `image_url` | Media | Imagenes alojadas por terceros, sujetas a disponibilidad y derechos |
| `cardmarket_price` | Media | Precio de mercado europeo, puede cambiar rapidamente |
| `tcgplayer_price` | Media | Precio de mercado estadounidense, puede cambiar rapidamente |
| `ebay_price` | Media | Precio de marketplace variable |
| `amazon_price` | Media | Precio de marketplace variable |
| `coolstuffinc_price` | Media | Precio de marketplace especifico |
| `card_price_history` | Media | Puede inducir conclusiones temporales si hay pocos snapshots |
| `ban_tcg`, `ban_ocg`, `ban_goat` | Baja-media | Afecta a interpretaciones competitivas |

La sensibilidad principal no es personal, sino comercial e interpretativa.

## 4. Implicaciones de privacidad

### 4.1 Ausencia de datos personales

El modelo no almacena:

- Nombres de usuarios.
- Correos electronicos.
- Direcciones.
- Metodos de pago.
- Historial de compra individual.
- Datos de comportamiento de clientes.

Esto reduce riesgos legales y eticos asociados a privacidad personal.

### 4.2 Dependencia de fuentes externas

Los datos proceden de sistemas publicos y marketplaces agregados por YGOPRODeck.

Implicacion:

El proyecto debe presentar los datos como informacion observada desde una fuente externa, no como datos propios ni garantizados.

### 4.3 Imagenes y URLs

Las imagenes y URLs son utiles para Power BI y presentaciones, pero no deben tratarse como activos propios.

Buenas practicas:

- Usarlas como referencia visual.
- Citar la procedencia.
- Evitar redistribuir imagenes como si fueran contenido propio.
- Considerar que las URLs pueden cambiar o dejar de funcionar.

### 4.4 Riesgo de inferencias comerciales

Aunque los datos sean publicos, el analisis puede generar recomendaciones.

Ejemplo:

- "Esta carta sube de precio".
- "Este set concentra valor".
- "Esta rareza parece mas rentable".

Estas conclusiones deben comunicarse como analisis exploratorio, no como asesoramiento financiero o garantia de mercado.

## 5. Calidad de los datos

La calidad de datos es central porque el modelo se usa para decisiones analiticas.

Dimensiones principales:

| Dimension | Pregunta clave |
|---|---|
| Completitud | Faltan campos importantes? |
| Exactitud | El dato representa correctamente la realidad? |
| Consistencia | Los datos mantienen el mismo criterio entre tablas? |
| Actualidad | Los datos estan actualizados? |
| Validez | Los valores cumplen el tipo y rango esperado? |
| Unicidad | Hay duplicados no deseados? |
| Trazabilidad | Se puede saber de donde viene el dato? |

## 6. Riesgos de calidad por tabla

### 6.1 `cards`

Riesgos:

- Campos opcionales nulos segun tipo de carta.
- Diferencias entre `card_type`, `human_readable_card_type` y `frame_type`.
- Descripciones largas o con caracteres especiales.

Control recomendado:

- Aceptar nulos donde la logica del juego lo justifique.
- No forzar atributos de monstruo en Spell/Trap.
- Mantener `card_id` como identificador estable.

### 6.2 `sets`

Riesgos:

- Variaciones de nombre de set.
- Dependencia de como la API publica el set.

Control recomendado:

- Usar `set_name` unico.
- Relacionar mediante `set_id` en `card_sets`.

### 6.3 `rarities`

Riesgos:

- Rarezas con nombres similares.
- Codigos incompletos o vacios.

Control recomendado:

- Mantener clave unica sobre `set_code`, `rarity_name`, `rarity_code`.
- No agrupar rarezas solo por nombre si el codigo aporta contexto.

### 6.4 `card_sets`

Riesgos:

- Redundancia controlada entre `set_name`, `set_rarity` y sus claves normalizadas.
- Precio `set_price` como valor de origen que puede no ser comparable con precios actuales.

Control recomendado:

- Usar claves ajenas para analisis relacional.
- Mantener campos textuales para trazabilidad.
- Documentar que `set_price` procede del contexto de set, no del precio actual por marketplace.

### 6.5 `card_prices`

Riesgos:

- Precios nulos.
- Diferentes monedas.
- Precios cambiantes.
- Diferencias metodologicas entre marketplaces.

Control recomendado:

- No mezclar EUR y USD sin conversion.
- Separar Cardmarket de marketplaces USD.
- Calcular promedios solo con valores no nulos.

### 6.6 `card_price_history`

Riesgos:

- Historico limitado a ejecuciones del ETL.
- Interpretacion incorrecta si hay pocos snapshots.
- Variaciones por datos faltantes.

Control recomendado:

- Verificar `COUNT(DISTINCT snapshot_at)`.
- Indicar intervalo temporal analizado.
- Evitar conclusiones predictivas con pocos registros.

### 6.7 `card_images`

Riesgos:

- URLs rotas.
- Multiples artes por carta.
- Dependencia de hosting externo.

Control recomendado:

- Tratar imagenes como apoyo visual, no como dato critico.
- Validar existencia de imagen principal cuando se use en dashboard.

### 6.8 `card_banlist`

Riesgos:

- Campo opcional.
- Formatos con reglas distintas.
- Cambios en restricciones.

Control recomendado:

- Diferenciar TCG, OCG y GOAT.
- No asumir que una carta sin banlist es siempre competitivamente valida.

### 6.9 `card_typelines` y `card_linkmarkers`

Riesgos:

- Orden de los elementos.
- Listas vacias en cartas que no aplican.

Control recomendado:

- Mantener `position`.
- No duplicar valores por carta.

## 7. Normalizacion y calidad

La normalizacion mejora la calidad porque separa entidades y reduce duplicados.

Beneficios:

- Una carta se almacena una vez en `cards`.
- Los sets se reutilizan desde `sets`.
- Las rarezas se reutilizan desde `rarities`.
- Las listas del JSON se convierten en tablas relacionales.
- Las relaciones se controlan mediante claves ajenas.

Riesgo:

Las consultas son mas complejas porque requieren `JOIN`.

Solucion:

Usar consultas SQL exploratorias y documentar la logica analitica antes de trasladarla a Power BI.

## 8. Controles recomendados

Controles basicos:

- Verificar numero de cartas cargadas.
- Comprobar nulos en precios.
- Comprobar duplicados por clave primaria.
- Verificar integridad referencial.
- Separar analisis por moneda.
- Validar numero de snapshots historicos.
- Documentar fecha de ingesta.
- Mantener copia raw del JSON descargado.

Consultas de control sugeridas:

```sql
SELECT COUNT(*) AS total_cards
FROM cards;
```

```sql
SELECT COUNT(*) AS prices_without_any_market
FROM card_prices
WHERE cardmarket_price IS NULL
  AND tcgplayer_price IS NULL
  AND ebay_price IS NULL
  AND amazon_price IS NULL
  AND coolstuffinc_price IS NULL;
```

```sql
SELECT COUNT(DISTINCT snapshot_at) AS total_snapshots
FROM card_price_history;
```

```sql
SELECT cs.card_id
FROM card_sets cs
LEFT JOIN cards c
    ON c.card_id = cs.card_id
WHERE c.card_id IS NULL;
```

## 9. Implicaciones para Power BI

Power BI debe mostrar los resultados con contexto.

Buenas practicas:

- Indicar fecha de ultima carga.
- Separar precios EUR y USD.
- Evitar mezclar marketplaces sin explicar la metrica.
- Mostrar el numero de snapshots si se presenta evolucion.
- Usar rankings como exploracion, no como verdad absoluta.
- Aclarar que los precios proceden de fuentes externas.

## 10. Conclusiones

El modelo tiene bajo riesgo de privacidad personal porque no almacena datos de usuarios ni transacciones individuales.

El riesgo principal esta en la calidad, actualidad e interpretacion de los datos.

Para que el analisis sea fiable, el proyecto debe:

- Mantener trazabilidad desde la API.
- Controlar nulos y duplicados.
- Separar monedas.
- Documentar fechas de carga.
- No presentar inferencias comerciales como certezas.
- Usar la normalizacion como base de consistencia.

En resumen, el modelo es adecuado para un proyecto formativo y analitico, siempre que las conclusiones se presenten como observaciones basadas en datos publicos y no como garantias de mercado.
