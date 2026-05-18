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

## Estructura inicial

```text
proyecto_SQL-DB_Yu-Gi-Oh/
├── docs/
├── notebooks/
├── sql/
├── src/
│   └── database/
│       ├── connection.py
│       └── create_tables.py
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

## Documentacion generada

- `docs/api_json_analysis.md`: analisis de estructura del JSON de YGOPRODeck y entidades candidatas para SQL.
