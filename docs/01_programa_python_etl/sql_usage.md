# Uso SQL

## Crear estructura

Paso previo manual en MySQL:

```text
Crear el schema yugioh_db.
```

Despues ejecutar:

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

`schema.sql` crea las tablas madre del proyecto dentro de `yugioh_db`.

## Usuario de ETL

El ETL debe conectarse con un usuario MySQL de privilegios limitados, no con `root`.

Usuario recomendado:

```text
pepin
```

Permisos necesarios para la carga normal:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
ON yugioh_db.*
TO 'pepin'@'localhost';

FLUSH PRIVILEGES;
```

`root` queda reservado para administracion: crear usuarios, crear schema y ejecutar cambios estructurales cuando sean necesarios.

En `.env`, el programa debe usar:

```env
DB_USER=pepin
DB_PASSWORD=<password_local_de_pepin>
```

`.env` no se versiona.

## Actualizar datos

```powershell
python -m src.etl
```

El ETL descarga datos desde la API, transforma el JSON y carga las tablas madre.

## Comprobacion basica

```sql
USE yugioh_db;
SHOW TABLES;
DESCRIBE cards;
```

## Tablas madre

```text
cards
sets
rarities
card_sets
card_images
card_prices
card_price_history
card_banlist
card_typelines
card_linkmarkers
```
