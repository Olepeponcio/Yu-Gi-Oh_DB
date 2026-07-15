# Panel operativo Tkinter

## Arranque

Desde la raíz del proyecto y con el entorno virtual activo:

```powershell
python -m src.control_panel
```

También puede usarse directamente el intérprete del proyecto:

```powershell
.\.venv\Scripts\python.exe -m src.control_panel
```

## Orden operativo

La ventana conserva el ciclo estructural 1→6, pero el botón 3 permanece habilitado desde el inicio como acceso directo para la carga rutinaria. Una carga directa correcta no obliga a ejecutar 4–6 ni altera el paso pendiente del ciclo estructural. Cada paso estructural libera exclusivamente a su sucesor; un error mantiene el mismo paso para repetirlo.

1. **Preparar DB + schema**: crea la base si falta, respalda `card_price_history`, elimina/recrea tablas desde `schema.sql` y restaura el histórico. Requiere confirmación visual.
2. **Validar API (dry-run)**: prueba API, cambio EUR/USD, transformación y calidad sin escribir en MySQL.
3. **ETL API + snapshot**: descarga el raw, carga tablas madre, inserta observaciones con un `snapshot_at` nuevo y genera backup del histórico.
4. **ETL raw + snapshot**: reproduce `data/raw/cardinfo_latest.json` y también inserta snapshot. Debe usarse conscientemente porque una ejecución real siempre amplía el histórico.
5. **Backup de snapshots**: exporta el histórico sin modificar la base.
6. **Ejecutar tests**: valida el código sin ejecutar reset ni carga.

## Seguridad

- Solo se ejecuta una acción simultánea.
- Los comandos se muestran en la consola integrada.
- El reset exige confirmación.
- La ventana permanece activa mientras el proceso trabaja en segundo plano.
- Cerrar la ventana no se usa como mecanismo para cancelar procesos.
- Las credenciales siguen procediendo del `.env`; no se guardan en la interfaz.
- El reset no crea ni elimina views. Las views antiguas con un `DEFINER` administrativo deben retirarse una sola vez desde MySQL con ese usuario.

## Diseño visual

- Paleta obtenida de `assets/palette.txt`.
- Playfair Display para títulos y Geomini para controles, textos y consola.
- Fuentes registradas de forma privada para el proceso desde `assets/fonts`; no se instalan en Windows.
- Ventana con opacidad `0.98`; el fondo claro derivado de Light Bronze aumenta la sensación traslúcida sin reducir la legibilidad de la consola.
- Bordes negros minimalistas de 1 px.
- El título `MySQL + ETL` alterna los cinco colores de la paleta letra por letra.
- El botón 3 es la acción principal: incorpora la etiqueta `ACCIÓN RECOMENDADA`, mayor altura y Playfair Display para guiar la carga habitual desde API con snapshot.
- Los botones bloqueados se muestran en gris; el color de paleta identifica el paso habilitado.

## Ampliaciones

Los botones se registran en `src/control_panel/actions.py`. Una ampliación debe declarar clave, texto, descripción, comando, color y si es destructiva o almacena snapshots. La ejecución y la interfaz permanecen desacopladas.
