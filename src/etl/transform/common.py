from decimal import Decimal, InvalidOperation


def to_int(value):
    if value is None or value == "":
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_decimal(value):
    if value is None or value == "":
        return None

    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def deduplicate_rows(rows, key_fields):
    deduplicated = {}

    for row in rows:
        key = tuple(row.get(field) for field in key_fields)
        deduplicated[key] = row

    return list(deduplicated.values())


def validate_required(row, required_fields, label):
    missing_fields = [field for field in required_fields if row.get(field) is None]

    if missing_fields:
        joined_fields = ", ".join(missing_fields)
        raise ValueError(f"{label} missing required fields: {joined_fields}")
