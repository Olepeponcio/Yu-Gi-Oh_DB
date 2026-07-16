# Panel operativo Tkinter

[Inicio](../../README.md) → [Programa Python y ETL](README.md) → Panel de control

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
- Sobre la consola, un indicador animado muestra la fase detectada y el tiempo
  transcurrido mientras el proceso sigue activo. Al terminar cambia a éxito o
  error; la barra es indeterminada porque el ETL no expone un porcentaje fiable.
- El reset exige confirmación.
- La ventana permanece activa mientras el proceso trabaja en segundo plano.
- Cerrar la ventana no se usa como mecanismo para cancelar procesos.
- Las credenciales siguen procediendo del `.env`; no se guardan en la interfaz.
- El reset no crea ni elimina views. Las views antiguas con un `DEFINER` administrativo deben retirarse una sola vez desde MySQL con ese usuario.

## Diseño visual

- Paleta obtenida de `assets/palette.txt`.
- Playfair Display para títulos y Geomini para controles, textos y consola.
- Fuentes registradas de forma privada para el proceso desde `assets/fonts`; no se instalan en Windows.
- El fondo negro usa una capa independiente con `alpha=0.75`: 75% de opacidad y 25% de transparencia. La capa superior mantiene botones, textos y consola totalmente opacos.
- Fondo y controles sincronizan posición, tamaño y orden Z.
- Ventana `topmost`: permanece por encima del resto de aplicaciones mientras está abierta.
- Bordes negros de 1 px limitados a botones y consola; sin marco exterior ni bordes en tarjetas.
- El título `MySQL + ETL` alterna Dusk Blue, Rosewood, Light Coral y Light Bronze sobre fondo negro.
- El botón 3 es la acción principal: incorpora la etiqueta `ACCIÓN RECOMENDADA`, mayor altura y Playfair Display para guiar la carga habitual desde API con snapshot.
- La consola muestra warnings en naranja, errores/crashes en rojo y procesos completados en verde.
- Los botones se iluminan suavemente al situar el ratón encima y recuperan su color original al salir.
- Los botones bloqueados se muestran en gris; el color de paleta identifica el paso habilitado.

## Ampliaciones

Los botones se registran en `src/control_panel/actions.py`. Una ampliación debe declarar clave, texto, descripción, comando, color y si es destructiva o almacena snapshots. La ejecución y la interfaz permanecen desacopladas.
