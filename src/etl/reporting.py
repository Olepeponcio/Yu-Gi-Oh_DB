def print_run_summary(metadata, snapshot_at, raw_path):
    print(f"Fuente: {metadata.get('source', 'raw file')}")
    print(f"Fecha de ingesta raw: {metadata.get('ingested_at', 'no disponible')}")
    print(f"Ultima actualizacion fuente: {metadata.get('source_last_updated') or 'no disponible'}")
    print(f"Snapshot de precios: {snapshot_at}")

    if raw_path is not None:
        print(f"JSON raw guardado: {raw_path}")


def print_table_counts(tables):
    for table_name, rows in tables.items():
        print(f"{table_name}: {len(rows)}")


def print_load_summary(affected):
    print("Carga MySQL completada.")
    for table, rowcount in affected.items():
        print(f"{table}: {rowcount}")
