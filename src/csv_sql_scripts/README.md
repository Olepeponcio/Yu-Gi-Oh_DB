# csv_sql_scripts

Utilidad auxiliar para una escalada futura del proyecto.

No forma parte del flujo principal ETL -> MySQL -> Power BI.

## Para que sirve

Lee CSV locales de:

```text
sql/analysis/CSV/
```

Y genera scripts SQL de recuperacion en:

```text
sql/generated/from_csv/
```

Cada script generado contiene:

```text
CREATE TABLE IF NOT EXISTS staging_...
CREATE OR REPLACE VIEW vw_... AS SELECT ... FROM staging_...
```

## Limites

- No conecta con MySQL.
- No ejecuta SQL.
- No lee `.env`.
- No sustituye las views oficiales de `sql/analysis/views/`.
- Recupera resultados CSV, no la logica SQL original.

## Uso

```powershell
python -m src.csv_sql_scripts --dry-run
python -m src.csv_sql_scripts
```
