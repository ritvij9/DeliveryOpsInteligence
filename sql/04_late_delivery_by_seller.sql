-- DeliveryOps Intelligence
-- One row per seller per order before aggregation.

WITH seller_orders AS (
    SELECT DISTINCT
        oi.seller_id,
        b.order_id,
        b.has_complete_delivery_dates,
        b.is_late_delivery,
        b.purchase_to_delivery_days,
        b.days_late_vs_estimate
    FROM read_parquet('data/processed/order_delivery_base.parquet') b
    JOIN read_csv_auto('data/raw/olist_order_items_dataset.csv') oi
        ON b.order_id = oi.order_id
),

seller_performance AS (
    SELECT
        seller_id,
        COUNT(*) AS total_orders,
        COUNT(*) FILTER (
            WHERE has_complete_delivery_dates
        ) AS eligible_orders,
        COUNT(*) FILTER (
            WHERE is_late_delivery
        ) AS late_orders,
        ROUND(
            100.0 * COUNT(*) FILTER (WHERE is_late_delivery)
            / NULLIF(
                COUNT(*) FILTER (WHERE has_complete_delivery_dates), 0
            ), 2
        ) AS late_delivery_rate_pct,
        ROUND(
            AVG(purchase_to_delivery_days)
            FILTER (WHERE has_complete_delivery_dates), 2
        ) AS avg_transit_days,
        ROUND(
            AVG(days_late_vs_estimate)
            FILTER (WHERE is_late_delivery), 2
        ) AS avg_days_late
    FROM seller_orders
    GROUP BY seller_id
)

SELECT *
FROM seller_performance
WHERE eligible_orders >= 100
ORDER BY late_delivery_rate_pct DESC, eligible_orders DESC;