
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "olist_geolocation_dataset.csv"


def main():
    df = pd.read_csv(FILE)

    zip_col = "geolocation_zip_code_prefix"
    lat_col = "geolocation_lat"
    lng_col = "geolocation_lng"

    print(f"Total rows: {len(df):,}")
    print(f"Distinct postal prefixes: {df[zip_col].nunique():,}")
    print(
        "Duplicate postal-prefix rows: "
        f"{df.duplicated(subset=[zip_col]).sum():,}"
    )
    print(
        "Distinct postal-prefix/coordinate combinations: "
        f"{df[[zip_col, lat_col, lng_col]].drop_duplicates().shape[0]:,}"
    )
    print(
        "Duplicate postal-prefix/coordinate rows: "
        f"{df.duplicated(subset=[zip_col, lat_col, lng_col]).sum():,}"
    )

    print("\n--- Postal prefixes with the most records ---")
    print(
        df[zip_col]
        .value_counts()
        .head(10)
        .rename_axis("postal_prefix")
        .reset_index(name="row_count")
        .to_string(index=False)
    )

    print("\n--- Example records for one repeated prefix ---")
    repeated_prefixes = df.loc[
        df.duplicated(subset=[zip_col], keep=False), zip_col
    ]

    if not repeated_prefixes.empty:
        example_prefix = repeated_prefixes.iloc[0]
        print(
            df.loc[df[zip_col] == example_prefix]
            .head(10)
            .to_string(index=False)
        )


if __name__ == "__main__":
    main()
