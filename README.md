# Proyecto SQL DB Yu-Gi-Oh

Proyecto de datos para construir una base MySQL relacional de cartas de Yu-Gi-Oh desde la API de YGOPRODeck, analizarla con SQL y comunicar resultados en Power BI.

## Piezas del proyecto

```text
sql/main_schema.sql        -> esquema principal vigente para crear la DB desde cero
sql/migrations/           -> reservado para futuras escaladas del modelo
sql/reset_main_schema.sql -> reinicio destructivo de tablas principales
sql/analysis/             -> consultas analiticas, reglas en validacion y CSV auxiliares
src/api/                  -> extraccion desde YGOPRODeck
src/etl/                  -> transformacion y carga en MySQL
src/database/             -> conexion Python -> MySQL
data/raw/                 -> ultimo JSON raw descargado
docs/                     -> documentacion tecnica y analitica
powerbi/                  -> documentacion, consultas y plantillas Power BI
```

## Idea clave

```text
MySQL relacional = fuente unica de verdad
SQL queries = exploracion, diagnostico y reglas en validacion
Power BI = modelo semantico, relaciones, medidas y narrativa
```

El proyecto vuelve al punto base: conservar tablas madre limpias en MySQL y construir el modelo semantico al conectar desde Power BI. No hay capa SQL intermedia oficial.

## Flujo general

```text
1. MySQL crea la estructura desde sql/main_schema.sql
2. Python ETL extrae datos de YGOPRODeck
3. Python transforma y normaliza datos
4. Python carga/actualiza tablas madre en MySQL
5. SQL queries convierten hechos en preguntas, controles y decisiones
6. Power BI importa tablas base y construye el modelo semantico
7. Power BI define relaciones, medidas, clasificaciones y narrativa
```

## Herramientas necesarias

- MySQL Server local.
- Cliente MySQL, MySQL Workbench o terminal MySQL.
- Python con dependencias de `requirements.txt`.
- Archivo `.env` con credenciales MySQL.
- Power BI Desktop para construir el modelo y exportar plantilla `.pbit`.

## 0. Preparar entorno Python

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 1. Configurar conexion

Crear `.env` a partir de `.env.example`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=yugioh_db
DB_USER=tu_usuario
DB_PASSWORD=tu_password
```

## 2. Construir la base desde cero

```sql
CREATE DATABASE IF NOT EXISTS yugioh_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE yugioh_db;
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/main_schema.sql;
```

Tablas madre vigentes:

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

No uses `reset_main_schema.sql` salvo que quieras borrar tablas y datos para reconstruir desde cero.

## 3. Probar el ETL

Sin escribir en MySQL:

```powershell
python -m src.etl --dry-run
```

Con JSON local:

```powershell
python -m src.etl --source file --raw-path data/raw/cardinfo_latest.json --dry-run
```

Tests:

```powershell
python -m unittest discover
```

## 4. Cargar o actualizar datos

```powershell
python -m src.etl
```

Este comando descarga datos, actualiza `data/raw/cardinfo_latest.json`, normaliza entidades y carga MySQL. Tambien inserta snapshots en `card_price_history`.

## 5. Analisis y Power BI

Marco analitico:

```text
docs/02_marco_analisis_datos/README.md
```

Implementacion por capa:

```text
sql/analysis/README.md -> organizacion de queries y reglas SQL
powerbi/README.md      -> conexion a tablas base y modelo semantico Power BI
```

Las consultas SQL no sustituyen a las tablas madre. Sirven para convertir hechos en preguntas, controles de calidad, criterios de decision y validaciones.

## Orden rapido

```text
1. Crear yugioh_db
2. SOURCE sql/main_schema.sql
3. python -m src.etl --dry-run
4. python -m src.etl
5. Ejecutar queries de sql/analysis/ para validar preguntas y reglas
6. Conectar Power BI a tablas madre MySQL
7. Crear relaciones, medidas y clasificaciones en Power BI
8. Exportar plantilla `.pbit` sin datos cargados
```

## Documentacion

- [Indice tecnico](docs/README.md)
- [Versionado y flujo Git](docs/00_gestion_proyecto/versionado_y_flujo_git.md)
- [Flujo ETL](docs/01_programa_python_etl/etl_flow.md)
- [Uso SQL](docs/01_programa_python_etl/sql_usage.md)
- [Analisis JSON API](docs/02_marco_analisis_datos/api_json_analysis.md)
- [Modelo de datos](docs/02_marco_analisis_datos/data_model.md)
