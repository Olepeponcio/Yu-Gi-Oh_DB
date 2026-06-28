# Versionado y flujo Git

Documento marco para normalizar el trabajo del repositorio desde el estado actual, sin reescribir el historico previo.

## Punto de control inicial

Desde el 23/05/2026 el proyecto adopta un flujo formal de ramas y versionado SemVer.

Punto base:

```text
version: v0.1.0
commit previo a la normalizacion: 7f03608
rama base: main
criterio: estado consolidado previo a la normalizacion del flujo Git
```

La etiqueta `v0.1.0` marca el inicio formal del modelo de trabajo. No implica que el proyecto sea estable a nivel final. Significa que existe una base funcional y documentada sobre la que se trabajara de forma ordenada.

## Historico previo

Hasta `v0.1.0`, el repositorio evoluciono de forma poco organizada según buenas practicas. Ese historico se conserva como trazabilidad real del proyecto.

Hitos principales identificados:

```text
9109b7f -> estructura inicial del proyecto y entorno de trabajo
5dc9939 -> analisis inicial del JSON de la API
f7f4534 -> primer esquema SQL principal
67fe8e6 -> primeras piezas ETL
0d71791 -> migraciones y limpieza de registros JSON
32ee90d -> estructura base desde schema.sql
a43dc6b -> utilidad auxiliar para cargar SQL desde CSV
2422db4 -> modularizacion del paquete ETL
196b0ca -> generacion de reporting
14a6a0a -> paquete modular de transformacion
5bbade4 -> refactor ETL y cambio de cards.id a cards.card_id
a69ebff -> refactor de schema y reporting en database
af789ea -> enriquecimiento de capa analitica con codigos de set
7f03608 -> organizacion de artefactos SQL de analisis
```

Ramas historicas existentes:

```text
analisis_JSON_API
estructura_SQL
cargaCSV
```

Estas ramas quedan como referencia historica. No forman parte del flujo nuevo salvo que se decida recuperar alguna idea concreta.

## Modelo de ramas desde ahora

```text
main                 -> rama estable y versionada
develop              -> integracion de trabajo antes de versionar
feature/*            -> nuevas funcionalidades
fix/*                -> correcciones de errores
refactor/*           -> mejoras internas sin cambio funcional esperado
docs/*               -> documentacion
release/vX.Y.Z       -> preparacion de una version concreta
```

Reglas:

- `main` debe representar estados funcionales y verificables.
- `develop` recibe el trabajo integrado antes de preparar una release.
- Las ramas de trabajo nacen desde `develop`.
- Las releases nacen desde `develop` y terminan fusionandose en `main`.
- No se reescribe el historico publicado salvo decision explicita y justificada.

## Versionado SemVer

Formato:

```text
vMAJOR.MINOR.PATCH
```

Criterio:

- `MAJOR`: cambios incompatibles o redisenos profundos del modelo.
- `MINOR`: nuevas capacidades compatibles.
- `PATCH`: correcciones pequenas, documentacion o ajustes sin impacto estructural.

Mientras el proyecto este en fase de construccion se usaran versiones `0.x.x`.

Ejemplos:

```text
v0.1.0 -> punto base normalizado
v0.2.0 -> nueva funcionalidad relevante
v0.2.1 -> correccion menor sobre v0.2.0
v1.0.0 -> primera version estable completa
```

## Flujo practico

Crear una rama de trabajo:

```powershell
git checkout develop
git checkout -b feature/nombre-corto
```

Trabajar con commits claros:

```powershell
git add .
git commit -m "feat: describir cambio"
```

Integrar en `develop`:

```powershell
git checkout develop
git merge feature/nombre-corto
```

Preparar una version:

```powershell
git checkout develop
git checkout -b release/v0.2.0
```

Cerrar version:

```powershell
git checkout main
git merge release/v0.2.0
git tag v0.2.0
git checkout develop
git merge main
```

## Convencion de commits

Usar mensajes cortos con prefijo:

```text
feat: nueva funcionalidad
fix: correccion de error
docs: documentacion
refactor: cambio interno sin cambio funcional esperado
test: pruebas
chore: tareas auxiliares
db: cambios SQL, modelo de datos o scripts de base de datos
```

Ejemplos:

```text
feat: anadir carga incremental de precios
fix: corregir normalizacion de nombres de set
db: actualizar consulta de rarezas por precio
docs: documentar flujo de versionado
refactor: separar transformaciones de precios
```

## Criterio de seguridad

El modelo se aplica hacia adelante:

```text
historico manual existente
    -> etiqueta v0.1.0
    -> rama develop
    -> flujo formal de ramas y versiones
```

No se reorganizan commits antiguos mediante rebase. La trazabilidad previa se documenta y se conserva.
