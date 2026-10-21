
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def load(name):
    return pd.read_csv(RAW / name, low_memory=False)


def check_unique(df, table, key):
    duplicates = int(df.duplicated(subset=key).sum())
    print(
        f"{table}: key={key}, rows={len(df):,}, "
        f"duplicate-key rows={duplicates:,}"
    )


def check_foreign_key(child, child_col, parent, parent_col, label):
    child_values = child[child_col].dropna()
    parent_values = set(parent[parent_col].dropna())

    orphan_count = int((~child_values.isin(parent_values)).sum())

    print(
        f"{label}: child rows={len(child_values):,}, "
        f"unmatched rows={orphan_count:,}"
    )


def main():
    customers = load("olist_customers_dataset.csv")
    orders = load("olist_orders_dataset.csv")
    items = load("olist_order_items_dataset.csv")
    payments = load("olist_order_payments_dataset.csv")
    reviews = load("olist_order_reviews_dataset.csv")
    products = load("olist_products_dataset.csv")
    sellers = load("olist_sellers_dataset.csv")

    print("\n--- Candidate key checks ---")
    check_unique(customers, "customers", ["customer_id"])
    check_unique(orders, "orders", ["order_id"])
    check_unique(orders, "orders", ["customer_id"])
    check_unique(items, "order_items", ["order_id", "order_item_id"])
    check_unique(payments, "payments", ["order_id", "payment_sequential"])
    check_unique(reviews, "reviews", ["review_id"])
    check_unique(reviews, "reviews", ["order_id"])
    check_unique(products, "products", ["product_id"])
    check_unique(sellers, "sellers", ["seller_id"])

    print("\n--- Foreign-key relationship checks ---")
    check_foreign_key(
        orders, "customer_id", customers, "customer_id",
        "orders -> customers"
    )
    check_foreign_key(
        items, "order_id", orders, "order_id",
        "order_items -> orders"
    )
    check_foreign_key(
        items, "product_id", products, "product_id",
        "order_items -> products"
    )
    check_foreign_key(
        items, "seller_id", sellers, "seller_id",
        "order_items -> sellers"
    )
    check_foreign_key(
        payments, "order_id", orders, "order_id",
        "payments -> orders"
    )
    check_foreign_key(
        reviews, "order_id", orders, "order_id",
        "reviews -> orders"
    )


if __name__ == "__main__":
    main()
