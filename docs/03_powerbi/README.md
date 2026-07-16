# Power BI — reinicio del modelo semántico

[Inicio](../../README.md) → [Documentación](../README.md) → Power BI

Las views y el diagrama anteriores se retiraron porque cruzaban precios de carta con rarezas de impresión mediante `card_id`, generando atribuciones y outliers falsos.

Estado actual:

```text
MySQL: tablas madre normalizadas
Views: pendientes de diseño
Power BI: retirar tablas y relaciones del modelo anterior
```

## Contrato para la siguiente fase

- Dirección de filtro única desde dimensiones hacia hechos.
- No relacionar hechos entre sí.
- Precio general: carta + marketplace + moneda + snapshot.
- Precio por rareza: únicamente precio de impresión.
- Promedios, rankings, variaciones y outliers se crearán como medidas, no como hechos agregados paralelos.
- No mezclar EUR y USD sin conversión explícita.

Los exports e informes existentes se conservan como evidencia histórica, no como contrato vigente.

Las nuevas tablas de consumo se definirán desde el [registro modular de views](../02_marco_analisis_datos/view_design/README.md). Power BI no debe incorporar una candidata hasta que su estado sea `validada`.
