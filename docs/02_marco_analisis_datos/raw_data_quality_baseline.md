# Línea base de calidad — `cardinfo_latest.json`

Fecha de auditoría: 2026-07-15.

```text
cartas: 14.458
impresiones raw: 44.004
sets únicos: 1.024
tipos de rareza normalizados: 38
observaciones de precio generadas: 72.290
```

## Rarezas apartadas o corregidas

```text
63  códigos numéricos internos: 2/3
108 etiquetas internas: New, Reprint, New artwork, debut, force-SMW
133 variantes tipográficas normalizadas
171 impresiones sin FK de rareza por calidad de fuente
```

No se detectaron nulos en `set_name`, `set_code`, `set_rarity`, `set_price` ni duplicados con el grano definitivo:

```text
card_id + set_code + raw_rarity_name + raw_rarity_code
```

Los 1.409 `set_rarity_code` vacíos son admitidos: el nombre de rareza existe y el código corto es opcional en la fuente.
