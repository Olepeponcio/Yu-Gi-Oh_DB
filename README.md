# Proyecto SQL DB Yu-Gi-Oh

Base del proyecto: programa Python + MySQL para extraer, transformar y cargar datos de cartas de Yu-Gi-Oh desde YGOPRODeck.

Este README explica como esta construido el programa y como llega hasta la creacion/carga de las tablas madre.

## 1. Objetivo del programa

```text
API YGOPRODeck -> JSON raw local -> transformacion Python -> tablas madre MySQL
```

El programa no contiene analisis consolidado. Su responsabilidad termina cuando MySQL queda cargado con el modelo relacional madre.

## 2. Estructura principal

```text
src/api/                  -> extraccion desde YGOPRODeck
src/etl/                  -> orquestacion ETL
src/etl/transform/        -> normalizacion por dominio
src/database/             -> conexion MySQL
sql/schema.sql            -> crea las tablas madre dentro de yugioh_db
docs/                     -> documentacion de trabajo
tests/                    -> pruebas del ETL
data/raw/                 -> JSON raw local
data/processed/           -> reservado para datos procesados locales
data/reporting/           -> reportes locales de ejecucion
data/backups/             -> backups locales restaurables de card_price_history
```

## 3. Modulos de `src`

### `src/api`

Responsabilidad: obtener datos desde YGOPRODeck.

Archivo principal:

```text
src/api/ygoprodeck_client.py
```

Hace:

- Llama al endpoint publico de cartas.
- Guarda una copia raw en `data/raw/cardinfo_latest.json`.
- Conserva metadatos de ingesta cuando estan disponibles.

### `src/database`

Responsabilidad: abrir conexion con MySQL.

Archivo principal:

```text
src/database/connection.py
```

Usa variables de `.env`:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

### `src/etl`

Responsabilidad: coordinar el flujo completo.

Entradas:

```text
src/etl/__main__.py
src/etl/main.py
src/etl/cli.py
```

Orquestacion:

```text
src/etl/pipeline.py
```

Carga:

```text
src/etl/load.py
```

Reporte:

```text
src/etl/reporting.py
src/etl/report_file.py
```

### `src/etl/transform`

Responsabilidad: convertir el JSON de la API en filas compatibles con MySQL.

```text
common.py     -> conversiones, validacion y deduplicacion
cards.py      -> carta base, imagenes y banlist
sets.py       -> sets, rarezas y apariciones carta-set
prices.py     -> precios actuales por marketplace
relations.py  -> typelines y linkmarkers
pipeline.py   -> coordinador de transformacion
```

## 4. Flujo ETL

```text
1. Leer argumentos de CLI.
2. Descargar JSON o leer JSON local.
3. Normalizar entidades.
4. Validar claves y campos requeridos.
5. Insertar/actualizar tablas madre.
6. Registrar snapshot de precios en card_price_history.
7. Emitir resumen de ejecucion.
```

### Panel operativo Tkinter

El flujo completo también puede manejarse desde una ventana local:

```powershell
python -m src.control_panel
```

El panel ordena preparación de DB/schema, validación dry-run, ETL API con snapshot, replay raw con snapshot, backup histórico y tests. Al inicio solo habilita el paso 1; cada ejecución correcta libera su sucesor y el paso 6 reinicia el ciclo. El reset requiere confirmación y la salida se muestra sin bloquear la ventana.

Documentación: `docs/01_programa_python_etl/control_panel.md`.

### Diseño modular de views

Antes de escribir SQL, cada view se registra por pregunta, grano, claves, medidas y riesgos en:

```text
docs/02_marco_analisis_datos/view_design/README.md
```

Ramas de análisis:

```text
01_descriptive → 02_diagnostic → 03_predictive → 04_prescriptive
```

## 5. Tablas madre

`sql/schema.sql` crea:

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

Regla de rarezas:

```text
card_printings.raw_rarity_name       -> valor literal recibido desde la API
card_printings.rarity_id             -> FK solo cuando la rareza es valida
card_printings.rarity_source_quality -> calidad del dato fuente
```

Si la API devuelve un indice numerico en `set_rarity`, por ejemplo `2` o `3`, el ETL conserva el literal, deja `rarity_id` en `NULL` y marca `rarity_source_quality = invalid_numeric_source`.

## 6. Preparar entorno

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configurar `.env` desde `.env.example`.

Regla de seguridad:

- El ETL debe conectarse con un usuario MySQL limitado, por ejemplo `etl_user`.
- No usar `root` para ejecutar cargas normales.
- `.env` guarda las credenciales locales y no se versiona.

## 7. Preparar MySQL

Proceso base:

- Crear manualmente el schema `yugioh_db` en MySQL.
- Ejecutar `sql/schema.sql` para crear las tablas madre.
- Conceder al usuario de ETL permisos limitados sobre `yugioh_db`.
- Ejecutar el ETL para cargar o actualizar datos desde la API.
- Si cambia la estructura de tablas madre, resetear/recrear la DB desde `sql/schema.sql`.
- No usar scripts incrementales como contrato estructural del proyecto.

```sql
SOURCE C:/ruta/al/proyecto/proyecto_SQL-DB_Yu-Gi-Oh/sql/schema.sql;
```

## 8. Ejecutar

Prueba sin escribir:

```powershell
python -m src.etl --dry-run
```

Carga completa:

```powershell
python -m src.etl
```

Desde JSON local:

```powershell
python -m src.etl --source file --raw-path data/raw/cardinfo_latest.json
```

Tests:

```powershell
python -m unittest discover
```

## 9. Reset seguro con historico

`card_price_history` es la tabla critica para el analisis predictivo. Antes de resetear tablas madre, hay que exportarla a un backup restaurable.

### Una sola linea

Desde PowerShell, en la raiz del proyecto:

```powershell
python -m src.etl.reset_mysql --yes
```

Hace, en este orden:

```text
1. Crea yugioh_db si no existe.
2. Si existe card_price_history, crea backup en data/backups/card_price_history/.
3. Ejecuta sql/drop_tables.sql.
4. Ejecuta sql/schema.sql.
5. Restaura automaticamente el backup de card_price_history.
```

Despues ejecutar la carga:

```powershell
python -m src.etl
```

El flag `--yes` es obligatorio porque el proceso borra y recrea tablas madre.

### Orden correcto

#### 1. Crear backup de `card_price_history`

Desde PowerShell, en la raiz del proyecto:

```powershell
python -m src.etl.history_backup backup
```

El backup queda en:

```text
data/backups/card_price_history/
```

#### 2. Resetear tablas madre en MySQL Workbench

En Workbench no se escribe la ruta del archivo en el editor SQL. Hay que abrir cada archivo y ejecutar su contenido.

Ejecutar en este orden:

```text
File -> Open SQL Script... -> sql/drop_tables.sql -> rayo ejecutar
File -> Open SQL Script... -> sql/schema.sql -> rayo ejecutar
```

Equivalencia del proceso:

```text
drop_tables.sql          -> borra tablas madre, incluida card_price_history
schema.sql               -> recrea tablas madre
```

#### 3. Restaurar el backup de `card_price_history`

Desde PowerShell:

```powershell
python -m src.etl.history_backup restore data/backups/card_price_history/card_price_history_YYYYMMDD_HHMMSS.sql
```

Sustituir `YYYYMMDD_HHMMSS` por el nombre real del archivo generado.

#### 4. Ejecutar nueva carga ETL

```powershell
python -m src.etl
```

### Regla operativa

```text
backup -> drop_tables.sql -> schema.sql -> restaurar card_price_history -> carga ETL
```

### Comprobacion

En MySQL Workbench:

```sql
USE yugioh_db;

SELECT snapshot_at, COUNT(*)
FROM card_price_history
GROUP BY snapshot_at
ORDER BY snapshot_at;
```

Cada carga ETL real genera automaticamente un nuevo backup de `card_price_history` en:

```text
data/backups/card_price_history/
```

## 10. README principales

```text
README.md                              -> programa Python y ETL hasta tablas madre
docs/02_marco_analisis_datos/README.md -> diario del proceso de analisis
docs/03_powerbi/README.md              -> proceso de trabajo en Power BI
power_bi/                              -> assets e informes Power BI del proyecto
```
