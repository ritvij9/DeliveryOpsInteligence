
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "raw" / "olist_order_reviews_dataset.csv"


def main():
    df = pd.read_csv(FILE)

    print(f"Total review rows: {len(df):,}")
    print(f"Distinct review IDs: {df['review_id'].nunique():,}")
    print(f"Distinct order IDs: {df['order_id'].nunique():,}")

    print("\n--- Most repeated review IDs ---")
    repeated_review_ids = df[
        df.duplicated("review_id", keep=False)
    ].sort_values("review_id")

    print(repeated_review_ids.head(12).to_string(index=False))

    print("\n--- Most repeated order IDs ---")
    repeated_order_ids = df[
        df.duplicated("order_id", keep=False)
    ].sort_values("order_id")

    print(repeated_order_ids.head(12).to_string(index=False))

    print("\n--- Exact duplicate review rows ---")
    print(df.duplicated().sum())


if __name__ == "__main__":
    main()
