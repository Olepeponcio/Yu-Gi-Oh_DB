# 04 — Prescriptive

[Inicio](../../../../README.md) → [Diseño de views](../README.md) → Prescriptive

## Propósito

Convertir evidencias descriptivas, diagnósticas y temporales en señales revisables. No generar recomendaciones automáticas desde un ranking aislado.

## Preguntas guía

- ¿Qué cartas presentan señales validadas para seguimiento prioritario?
- ¿Qué oportunidades deben permanecer en revisión antes de convertirse en recomendación?

La evidencia, vigencia, cobertura, legalidad y excepciones se documentan dentro de cada regla; no generan preguntas separadas.

## Requisitos previos

- Views base validadas.
- Medidas descriptive y diagnostic aprobadas.
- Cobertura histórica mínima definida.
- Reglas de negocio versionadas.
- Estados de banlist interpretados por ámbito.

## Candidata condicionada

### `vw_fact_card_monitoring_signals`

- Estado: bloqueada hasta aprobar reglas.
- Grano: carta + marketplace + moneda + snapshot + regla.
- Fuentes permitidas: hechos base y reglas explícitas.
- Salida mínima: identificadores, fecha, regla, valor observado, umbral y motivo.
- Prohibido: texto de “comprar/vender” sin revisión humana.
- Riesgo: convertir correlación o outlier en recomendación.
- Aceptación: toda señal debe ser reproducible y explicar qué regla la activó.

## Registro de decisión

Cada regla prescriptiva debe documentar:

```text
nombre → evidencia → umbral → excepciones → vigencia → responsable de revisión
```

Si una señal no puede explicar esos seis elementos, permanece en diagnostic y no avanza a prescriptive.
