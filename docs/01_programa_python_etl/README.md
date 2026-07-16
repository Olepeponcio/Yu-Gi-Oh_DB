# Programa Python y ETL

[Inicio](../../README.md) → Programa Python y ETL

Esta rama documenta cómo preparar, ejecutar y mantener el proceso de datos.

## Guías

1. [Panel de control](control_panel.md): entrada recomendada, botones, orden y
   seguridad operativa.
2. [Flujo ETL](etl_flow.md): módulos, transformación, datos raw y formas de
   ejecución.
3. [Uso de MySQL](sql_usage.md): estructura, usuario limitado, permisos y
   comprobaciones.

## Comandos esenciales

```powershell
python -m src.control_panel
python -m src.etl --dry-run
python -m src.etl
python -m unittest discover
```

Volver al [índice general de documentación](../README.md).
