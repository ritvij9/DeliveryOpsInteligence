
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = PROJECT_ROOT / "sql" / "01_order_delivery_base.sql"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "order_delivery_base.parquet"

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    sql = SQL_FILE.read_text(encoding="utf-8").strip().rstrip(";")

    con.execute(
        f"COPY ({sql}) TO '{OUTPUT_FILE.as_posix()}' (FORMAT PARQUET)"
    )

    result = con.execute(
        f"""
        SELECT
            COUNT(*) AS row_count,
            COUNT(DISTINCT order_id) AS unique_orders,
            COUNT(*) FILTER (WHERE is_late_delivery) AS late_orders
        FROM read_parquet('{OUTPUT_FILE.as_posix()}')
        """
    ).fetchone()

    print(f"Output: {OUTPUT_FILE}")
    print(f"Rows: {result[0]}")
    print(f"Unique orders: {result[1]}")
    print(f"Late orders: {result[2]}")

    con.close()

if __name__ == "__main__":
    main()
