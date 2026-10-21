
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "olist_geolocation_dataset.csv"


def main():
    df = pd.read_csv(FILE)

    zip_col = "geolocation_zip_code_prefix"

    summary = (
        df.groupby(zip_col)
        .agg(
            rows=(zip_col, "size"),
            distinct_cities=("geolocation_city", "nunique"),
            distinct_states=("geolocation_state", "nunique"),
            distinct_latitudes=("geolocation_lat", "nunique"),
            distinct_longitudes=("geolocation_lng", "nunique"),
        )
    )

    print(f"Postal prefixes: {len(summary):,}")
    print(
        "Prefixes with multiple cities: "
        f"{(summary['distinct_cities'] > 1).sum():,}"
    )
    print(
        "Prefixes with multiple states: "
        f"{(summary['distinct_states'] > 1).sum():,}"
    )
    print(
        "Prefixes with multiple latitudes: "
        f"{(summary['distinct_latitudes'] > 1).sum():,}"
    )
    print(
        "Prefixes with multiple longitudes: "
        f"{(summary['distinct_longitudes'] > 1).sum():,}"
    )

    print("\n--- Prefixes with the most city variation ---")
    print(
        summary.sort_values(
            ["distinct_cities", "rows"], ascending=False
        )
        .head(10)
        .to_string()
    )


if __name__ == "__main__":
    main()
