
WITH seller_state_orders AS (
    SELECT DISTINCT
        oi.seller_id,
        c.customer_state,
        b.order_id,
        b.is_late_delivery,
        b.purchase_to_delivery_days
    FROM read_parquet(
        'data/processed/order_delivery_base.parquet'
    ) b
    JOIN read_csv_auto(
        'data/raw/olist_order_items_dataset.csv'
    ) oi
        ON b.order_id = oi.order_id
    JOIN read_csv_auto(
        'data/raw/olist_customers_dataset.csv'
    ) c
        ON b.customer_id = c.customer_id
    WHERE b.has_complete_delivery_dates
)

SELECT
    seller_id,
    customer_state,
    COUNT(*) AS eligible_orders,
    COUNT(*) FILTER (
        WHERE is_late_delivery
    ) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_late_delivery)
        / COUNT(*), 2
    ) AS late_rate_pct,
    ROUND(AVG(purchase_to_delivery_days), 2) AS avg_transit_days
FROM seller_state_orders
GROUP BY seller_id, customer_state
HAVING COUNT(*) >= 30
ORDER BY late_rate_pct DESC, eligible_orders DESC;
