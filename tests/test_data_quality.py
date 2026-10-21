
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def load(name):
    return pd.read_csv(RAW / name)


def test_order_ids_are_unique():
    orders = load("olist_orders_dataset.csv")
    assert not orders["order_id"].duplicated().any()


def test_order_item_composite_key_is_unique():
    items = load("olist_order_items_dataset.csv")
    assert not items.duplicated(
        subset=["order_id", "order_item_id"]
    ).any()


def test_payment_composite_key_is_unique():
    payments = load("olist_order_payments_dataset.csv")
    assert not payments.duplicated(
        subset=["order_id", "payment_sequential"]
    ).any()


def test_order_items_reference_existing_orders():
    items = load("olist_order_items_dataset.csv")
    orders = load("olist_orders_dataset.csv")

    assert items["order_id"].isin(orders["order_id"]).all()


def test_order_items_reference_existing_products():
    items = load("olist_order_items_dataset.csv")
    products = load("olist_products_dataset.csv")

    assert items["product_id"].isin(products["product_id"]).all()


def test_order_items_reference_existing_sellers():
    items = load("olist_order_items_dataset.csv")
    sellers = load("olist_sellers_dataset.csv")

    assert items["seller_id"].isin(sellers["seller_id"]).all()
