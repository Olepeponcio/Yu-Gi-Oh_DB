# Constructor del informe Power BI

Este README define como usar y mantener `build_powerbi_report.py`.

## Finalidad

`build_powerbi_report.py` es la fuente reproducible del informe Word de desarrollo.

Genera:

```text
docs/03_powerbi/informe_desarrollo/informe_analisis_powerbi_yugioh.docx
```

No pertenece al ETL ni modifica datos. Su funcion es documentar el hilo de Power BI.

## Regla principal

El archivo `.py` manda.

Si se ejecuta el constructor, el DOCX se regenera desde el codigo. Por tanto:

- Si quieres actualizar el informe Word, el contenido debe cambiarse en `build_doc()`.
- El `.docx` es salida generada; el `.py` es la fuente mantenible.
- Este constructor no genera `modelo_relacional_powerbi.png`.

## Uso normal

Desde la raiz del proyecto:

```powershell
python docs\03_powerbi\informe_desarrollo\build_powerbi_report.py
```

Con el Python de Codex:

```powershell
C:\Users\PEPIN\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\03_powerbi\informe_desarrollo\build_powerbi_report.py
```

Resultado esperado:

```text
informe_analisis_powerbi_yugioh.docx
```

## Bloqueo por Word

Si `informe_analisis_powerbi_yugioh.docx` esta abierto en Word, Windows puede bloquear la sobrescritura.

Proceso:

1. Cerrar el Word.
2. Ejecutar otra vez el constructor.
3. Abrir de nuevo el `.docx`.

El script tiene una salida alternativa si hay bloqueo, pero la pauta recomendada es cerrar Word y regenerar el archivo principal.

## Como actualizar el informe Word

Editar esta funcion:

```text
build_doc()
```

Dentro de esa funcion se definen las secciones del informe:

- Portada.
- Indice.
- Resumen ejecutivo.
- Objetivos.
- Descripcion de datos.
- Preparacion de datos.
- Modelo Power BI.
- Vistas de consumo.
- Analisis descriptivo.
- Analisis diagnostico.
- Analisis predictivo.
- Analisis prescriptivo.
- Conclusiones.
- Limitaciones.
- Trabajo futuro.
- Anexos.

Proceso recomendado:

1. Localizar la seccion a actualizar en `build_doc()`.
2. Cambiar texto, tablas o listas.
3. Ejecutar:

```powershell
python docs\03_powerbi\informe_desarrollo\build_powerbi_report.py
```

4. Abrir el `.docx`.
5. En Word, actualizar campos si el indice no se actualiza automaticamente.

## Pautas para cambios

- No editar el `.docx` como fuente principal si el cambio debe conservarse.
- Cada nueva pagina de Power BI debe tener pregunta base, vista usada, medidas y estado.
- Cada nueva medida DAX debe registrarse en la seccion de medidas.
- Cada visual importante debe poder rastrearse a una vista SQL o tabla de consumo.
- Las conclusiones solo deben escribirse cuando existan visuales o consultas que las sostengan.

## Flujo de trabajo recomendado

```text
README / diario de analisis
        ↓
actualizar build_powerbi_report.py
        ↓
regenerar DOCX
        ↓
revisar resultado
        ↓
mantener el .py como fuente de verdad
```

## Que no debe hacer este constructor

- No debe ejecutar el ETL.
- No debe conectarse a MySQL.
- No debe calcular metricas de negocio.
- No debe sustituir a Power BI.
- No debe contener credenciales.

Su responsabilidad termina en generar documentacion reproducible.
