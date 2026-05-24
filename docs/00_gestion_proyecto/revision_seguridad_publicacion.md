# Revision de seguridad para publicacion publica

Revision orientada a publicar el repositorio como proyecto personal descargable.

Fecha de revision: 23/05/2026.

## Resultado

No se han encontrado credenciales reales ni datos sensibles trackeados en el estado actual del repositorio.

El archivo local `.env` existe en la maquina de desarrollo, pero no esta trackeado por Git y queda ignorado por `.gitignore`.

## Alcance revisado

Se reviso:

- Archivos trackeados actualmente por Git.
- Historial Git visible en todas las ramas locales/remotas.
- Patrones habituales de secretos: passwords, tokens, API keys, claves privadas y credenciales.
- Directorios locales de datos y reporting.
- Scripts SQL destructivos.
- Dependencias Python declaradas.

## Hallazgos

### Sin filtracion detectada

No aparece `.env` en el historial Git.

No aparecen credenciales reales en `.env.example`, `README.md` ni codigo Python. Los valores publicados son placeholders:

```text
tu_usuario
tu_password
```

Los datos locales de API y reportes ETL estan ignorados:

```text
data/raw/cardinfo_latest.json
data/reporting/etl_report_*.txt
```

### Riesgos corregidos

`.gitignore` se ha endurecido para evitar subidas accidentales de:

- `.env.*`, excepto `.env.example`.
- notebooks locales.
- datos bajo `data/`, conservando `.gitkeep`.
- dumps, backups y logs locales.

`requirements.txt` queda fijado con versiones concretas para reducir variacion entre instalaciones.

### Riesgos aceptados

`sql/reset_main_schema.sql` es destructivo porque borra tablas. Se conserva porque es una herramienta legitima de reconstruccion local y ya esta advertida en README y documentacion SQL.

La API usada es publica y no requiere token:

```text
https://db.ygoprodeck.com/api/v7/cardinfo.php
```

## Recomendaciones antes de publicar

1. No subir nunca `.env`, dumps SQL, notebooks con outputs ni datos raw locales.
2. Revisar `git status --short` antes de cada commit.
3. Ejecutar busqueda de secretos antes de releases publicas:

```powershell
rg -n -i "password|passwd|secret|token|api[_-]?key|credential|private[_-]?key|DB_PASSWORD|DB_USER" .
```

4. Si alguna credencial real fue expuesta fuera de Git, rotarla igualmente.
5. Crear usuarios MySQL locales con permisos limitados para pruebas y evitar usar `root`.

## Estado publico recomendado

El repositorio es apto para publicacion personal publica con las cautelas anteriores.

No requiere limpieza destructiva del historial Git segun la revision actual.
