# SQL de analisis

Directorio para scripts SQL de la fase analitica.

Uso previsto:

```text
sql/analysis/views/   -> scripts oficiales CREATE VIEW sobre tablas base MySQL
sql/analysis/CSV/     -> CSV locales exportados desde consultas previas, consumibles por Power BI como snapshots
```

Los scripts de `views/` se ejecutan desde MySQL sobre `yugioh_db` y quedan versionados en el proyecto.

## Criterio de uso

```text
views/ = logica SQL oficial para Power BI
CSV/ = resultados exportados, utiles como respaldo o fuente snapshot
sql/generated/from_csv/ = recuperacion auxiliar fuera de analysis
```

Power BI debe consumir preferentemente las views creadas en MySQL. Los CSV pueden usarse cuando interese trabajar con una foto fija del resultado.

## Utilidad auxiliar desde CSV

`src.csv_sql_scripts` puede generar scripts SQL de staging/view desde CSV locales:

```powershell
python -m src.csv_sql_scripts --dry-run
python -m src.csv_sql_scripts
```

Por cada CSV se crea un script en `sql/generated/from_csv/` con:

```text
CREATE TABLE IF NOT EXISTS staging_...
CREATE OR REPLACE VIEW vw_... AS SELECT ... FROM staging_...
```

El modulo solo genera archivos `.sql`; no conecta con MySQL ni ejecuta cambios en la base. Es una herramienta futura de recuperacion, no el flujo analitico principal.
