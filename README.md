# Proyecto SQL DB Yu-Gi-Oh

ETL en Python y MySQL para extraer datos de cartas desde YGOPRODeck,
normalizarlos y mantener un histórico de precios preparado para análisis en
Power BI.

## Estado del proyecto

- ETL y tablas madre: operativos.
- Panel de control local: operativo.
- Modelo analítico: en rediseño desde las tablas madre.
- Power BI: los informes existentes se conservan como evidencia histórica, no
  como contrato vigente.

## Inicio rápido

### 1. Clonar y preparar Python

Requiere Python 3 y una instancia local de MySQL.

```powershell
git clone <URL_DEL_REPOSITORIO>
cd proyecto_SQL-DB_Yu-Gi-Oh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copiar `.env.example` como `.env` y completar las credenciales locales. El
archivo `.env` no se versiona.

### 2. Abrir el panel de control

Esta es la entrada recomendada para preparar la base, validar la API, ejecutar
el ETL, crear backups y lanzar las pruebas:

```powershell
python -m src.control_panel
```

También puede ejecutarse sin activar el entorno:

```powershell
.\.venv\Scripts\python.exe -m src.control_panel
```

La explicación de cada botón y del orden operativo está en la
[guía del panel de control](docs/01_programa_python_etl/control_panel.md).

### 3. Ejecutar sin interfaz

```powershell
# Validar API y transformación sin escribir en MySQL
python -m src.etl --dry-run

# Carga completa desde la API
python -m src.etl

# Pruebas
python -m unittest discover
```

Para preparar o reconstruir las tablas:

```powershell
python -m src.etl.reset_mysql --yes
```

Este reset conserva `card_price_history`, pero actualmente requiere una cuenta
con permisos estructurales. El usuario limitado definido en
`sql/security_etl_user.sql` está destinado a las cargas normales.

## Arquitectura

```text
YGOPRODeck API
    ↓
data/raw/cardinfo_latest.json
    ↓
src/etl/transform/
    ↓
tablas madre MySQL + histórico de precios
    ↓
diseño de views → modelo Power BI
```

```text
src/api/           clientes YGOPRODeck y tipo de cambio ECB
src/database/      conexión y guardas de credenciales MySQL
src/etl/           CLI, pipeline, transformación, carga, reportes y backups
src/control_panel/ panel operativo Tkinter
sql/               contrato de tablas y seguridad
tests/             pruebas automatizadas
docs/              documentación por ramas
power_bi/          informes, exportaciones y recursos visuales
data/              datos locales, reportes y backups no versionados
```

## Documentación

La documentación parte de un único [índice general](docs/README.md):

1. [Programa Python y ETL](docs/01_programa_python_etl/README.md): instalación
   operativa, panel, flujo ETL y uso de MySQL.
2. [Marco de análisis de datos](docs/02_marco_analisis_datos/README.md): calidad,
   modelo relacional y diseño modular de views.
3. [Power BI](docs/03_powerbi/README.md): estado y reglas del modelo semántico.
4. [Contrato SQL](sql/README.md): tablas madre y futura organización de views.

## Seguridad y datos locales

- No versionar `.env`, JSON raw, reportes de ejecución ni backups.
- No usar `root` para cargas ETL normales.
- No habilitar bases remotas salvo mediante `DB_ALLOW_REMOTE_DB=true` de forma
  consciente.
- No ejecutar manualmente la secuencia `drop_tables.sql` + `schema.sql`; usar el
  reset automatizado para proteger el histórico.

## Fuente de verdad

`sql/schema.sql` define las tablas madre. Las views analíticas solo se incorporan
cuando su ficha de diseño y sus controles de calidad están validados.
