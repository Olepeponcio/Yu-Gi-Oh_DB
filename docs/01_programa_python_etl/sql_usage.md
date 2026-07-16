# Uso SQL

[Inicio](../../README.md) → [Programa Python y ETL](README.md) → Uso SQL

## Crear estructura

Usar el paso **Preparar DB + schema** del panel o su comando equivalente:

```powershell
python -m src.etl.reset_mysql --yes
```

El comando crea `yugioh_db` si falta, ejecuta `schema.sql` y protege el histórico
mediante backup y restauración. No ejecutar manualmente `drop_tables.sql` y
`schema.sql` como secuencia operativa.

Limitación actual: `reset_mysql` usa las credenciales del `.env` y necesita
`CREATE`, `DROP` y `ALTER`. El usuario limitado definido más abajo está pensado
para la carga ETL normal y no puede ejecutar el reset. Hasta separar credenciales
operativas y administrativas, hay que cambiar conscientemente de cuenta para esta
acción y volver después al usuario limitado.

Contrato de actualizacion estructural:

- Los cambios de columnas/tablas se incorporan en `sql/schema.sql`.
- Para aplicar un cambio estructural, se resetea/recrea la DB desde `sql/schema.sql`.
- No se usan scripts incrementales como contrato oficial de tablas madre.

## Usuario de ETL

El ETL debe conectarse con un usuario MySQL de privilegios limitados, no con `root`.

Usuario recomendado:

```text
<usuario_etl>
```

Script recomendado:

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/security_etl_user.sql;
```

Si el usuario `<usuario_etl>` no existe, MySQL generara una password aleatoria. Esa password debe copiarse solo al `.env` local.

Permisos necesarios para la carga normal:

```sql
GRANT SELECT, INSERT, UPDATE, DELETE
ON yugioh_db.*
TO '<usuario_etl>'@'localhost';

FLUSH PRIVILEGES;
```

`root` queda reservado para administracion: crear usuarios, crear schema y ejecutar cambios estructurales cuando sean necesarios.

En `.env`, el programa debe usar:

```env
DB_HOST=localhost
DB_USER=<usuario_etl>
DB_PASSWORD=<password_local_del_usuario_etl>
```

`.env` no se versiona.

Guardas aplicadas por el programa:

- Rechaza `DB_USER=root`.
- Rechaza `DB_HOST` remoto salvo que se declare explicitamente `DB_ALLOW_REMOTE_DB=true`.
- Usa placeholders SQL en la carga ETL; la password solo se lee desde `.env`.

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
rarity_types
card_printings
card_images
card_price_history
card_banlist
card_typelines
card_linkmarkers
```
