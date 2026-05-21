from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV_DIR = PROJECT_ROOT / "sql" / "analysis" / "CSV"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "sql" / "generated" / "from_csv"
STAGING_PREFIX = "staging_"
SQL_EXTENSION = ".sql"
