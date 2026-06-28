# Uso SQL

## Crear estructura

```sql
CREATE DATABASE IF NOT EXISTS yugioh_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

`main_schema.sql` crea las tablas madre del proyecto.

## Reset completo

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/RESET_SCHEMA.sql;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

`RESET_SCHEMA.sql` borra `yugioh_db` completa y la recrea vacia.

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
