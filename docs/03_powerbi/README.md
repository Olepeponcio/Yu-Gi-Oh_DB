# Proceso de trabajo en Power BI

Este README documentara el trabajo en Power BI cuando el analisis empiece a generar consultas de consumo.

## Punto de entrada

Power BI se conectara a MySQL:

```text
yugioh_db
```

La conexion no debe alterar las tablas madre. El modelado visual se construira desde las consultas que se vayan definiendo en el proceso de analisis.

## Fases de trabajo

| Fase | Entrada | Salida esperada | Estado | Notas |
|---|---|---|---|---|
| Conexion | MySQL `yugioh_db` | Origen configurado | Pendiente | Validar credenciales y tablas disponibles |
| Carga inicial | Tablas madre | Modelo preliminar | Pendiente | No crear relaciones ambiguas |
| Modelo | Consultas documentadas | Relaciones y medidas | Pendiente | Direccion de filtro controlada |
| Visualizacion | Medidas y campos validados | Paginas de informe | Pendiente | Cada pagina debe responder una pregunta |
| Publicacion | Archivo local de trabajo | Plantilla/documentacion | Pendiente | No versionar datos cargados |

## Reglas

- No mezclar monedas sin segmentacion.
- No usar `set_price` como precio de rareza.
- No crear decisiones desde rankings aislados.
- Documentar cada medida relevante.
- Mantener trazabilidad entre visual, consulta y pregunta del diario de analisis.

## Registro de paginas

| Pagina | Pregunta base | Consulta o tabla usada | Medidas | Estado | Notas |
|---|---|---|---|---|---|
|  |  |  |  | Pendiente |  |

## Registro de medidas

| Medida | Formula o descripcion | Tabla/consulta | Estado | Notas |
|---|---|---|---|---|
|  |  |  | Pendiente |  |
