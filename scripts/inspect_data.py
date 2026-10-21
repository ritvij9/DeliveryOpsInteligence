
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def inspect_csv(file_path: Path) -> None:
    print(f"\n{'=' * 70}")
    print(f"FILE: {file_path.name}")
    print("=" * 70)

    df = pd.read_csv(file_path, low_memory=False)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Completely duplicated rows: {df.duplicated().sum():,}")

    print("\nSchema and missing values:")

    schema = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean().values * 100).round(2),
        }
    )

    print(schema.to_string(index=False))


def main() -> None:
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(f"Raw data directory not found: {RAW_DATA_DIR}")

    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in: {RAW_DATA_DIR}")

    print(f"Project: {PROJECT_ROOT}")
    print(f"CSV files found: {len(csv_files)}")

    for file_path in csv_files:
        inspect_csv(file_path)


if __name__ == "__main__":
    main()
