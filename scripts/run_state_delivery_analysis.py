
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = ROOT / "sql" / "02_late_delivery_by_state.sql"


def main():
    query = SQL_FILE.read_text(encoding="utf-8")
    con = duckdb.connect()

    result = con.execute(query).fetchdf()

    print("=== STATE-LEVEL DELIVERY PERFORMANCE ===")
    print(result.to_string(index=False))

    print("\n=== STATES WITH AT LEAST 500 ELIGIBLE ORDERS ===")
    print(
        result.loc[result["eligible_orders"] >= 500]
        .sort_values("late_delivery_rate_pct", ascending=False)
        .to_string(index=False)
    )

    con.close()


if __name__ == "__main__":
    main()
