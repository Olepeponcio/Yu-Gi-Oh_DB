# Proyecto SQL DB Yu-Gi-Oh

Proyecto portfolio para aprender practicando un flujo ETL con Python y consultas SQL sobre MySQL.

El objetivo es construir una base de datos local con informacion de cartas de Yu-Gi-Oh, cargar datos mediante scripts Python y consultarlos con SQL de forma progresiva.

## Estado actual

Infraestructura base completada:

- Repositorio modular creado.
- `.gitignore` configurado para excluir entorno virtual, variables sensibles, cache y datos locales.
- `.env` local creado para credenciales privadas.
- `.env.example` creado como plantilla de configuracion.
- Entorno virtual `.venv` creado y activo.
- Dependencias instaladas en `requirements.txt`:
  - `requests`
  - `pandas`
  - `python-dotenv`
  - `mysql-connector-python`
- MySQL local reutilizado correctamente.
- Base de datos `yugioh_db` creada.
- Usuario dedicado para ETL creado: `yugioh_user`.
- Permisos del usuario corregidos sobre `yugioh_db`.
- Conexion Python -> MySQL validada desde `src/database/connection.py`.
- Muestra JSON de la API YGOPRODeck analizada antes de disenar el esquema SQL.
- Esquema SQL inicial creado y ejecutado manualmente en MySQL.
- Separado el reinicio destructivo del esquema en un archivo independiente.

## Estructura inicial

```text
proyecto_SQL-DB_Yu-Gi-Oh/
├── docs/
│   └── api_json_analysis.md
├── notebooks/
├── sql/
│   ├── schema.sql
│   └── reset_schema.sql
├── src/
│   └── database/
│       └── connection.py
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Flujo de trabajo realizado

1. Se preparo el repositorio con una estructura separada para codigo, SQL, documentacion y notebooks.
2. Se configuro un entorno virtual para aislar dependencias del sistema.
3. Se instalaron las librerias necesarias para:
   - conectar con MySQL,
   - leer variables de entorno,
   - consumir APIs,
   - manipular datos tabulares.
4. Se configuro MySQL local con una base de datos propia para el proyecto.
5. Se creo un usuario especifico para el proceso ETL, evitando usar el usuario administrador.
6. Se corrigieron permisos para que el usuario ETL pueda trabajar sobre `yugioh_db`.
7. Se implemento y valido una funcion reutilizable de conexion desde Python.
8. Se alineo `.env.example` con las variables usadas por `src/database/connection.py`:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
9. Se analizo una muestra real del endpoint `cardinfo.php` de YGOPRODeck para detectar campos principales, campos opcionales y listas anidadas.
10. Se diseno un primer esquema SQL normalizado, separando:
   - cartas,
   - sets,
   - imagenes,
   - precios,
   - banlist,
   - typeline,
   - linkmarkers.
11. Se dejo `sql/schema.sql` como archivo de creacion no destructiva usando `CREATE TABLE IF NOT EXISTS`.
12. Se movio la parte de borrado a `sql/reset_schema.sql` para evitar eliminar datos por accidente antes de cargas reales.

## Uso de SQL

### Crear estructura

Uso normal:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

Este archivo puede ejecutarse varias veces porque usa `CREATE TABLE IF NOT EXISTS`.
Si las tablas ya existen, MySQL no las vuelve a crear y no borra datos.

Comprobacion basica:

```sql
SHOW TABLES;
DESCRIBE cards;
```

### Reiniciar estructura

Uso destructivo:

```sql
USE yugioh_db;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/reset_schema.sql;
SOURCE C:/Users/PEPIN/D_JOSE/DESAROLLO/Proyectos/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

`reset_schema.sql` borra tablas y datos. Solo debe usarse en pruebas o cuando se quiera reconstruir la base desde cero.

### Cambios futuros

`schema.sql` sirve para crear la estructura inicial, pero no modifica tablas ya existentes.

Si mas adelante se anade una columna o se cambia una tabla, conviene crear archivos de migracion con `ALTER TABLE`, por ejemplo:

```text
sql/migrations/001_add_column_example.sql
```

## Documentacion generada

- `docs/api_json_analysis.md`: analisis de estructura del JSON de YGOPRODeck y entidades candidatas para SQL.
- `sql/schema.sql`: esquema inicial no destructivo.
- `sql/reset_schema.sql`: reinicio completo del esquema, destructivo.
