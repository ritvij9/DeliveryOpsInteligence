
-- DeliveryOps Intelligence
-- Question: How does late-delivery performance vary by customer state?
-- Grain: One row per customer state.
-- Denominator: Orders with actual and estimated delivery timestamps.

WITH order_delivery AS (
    SELECT
        order_id,
        customer_id,
        has_complete_delivery_dates,
        is_late_delivery
    FROM read_parquet('data/processed/order_delivery_base.parquet')
),

customer_orders AS (
    SELECT
        od.order_id,
        c.customer_state,
        od.has_complete_delivery_dates,
        od.is_late_delivery
    FROM order_delivery od
    INNER JOIN read_csv_auto(
        'data/raw/olist_customers_dataset.csv'
    ) c
        ON od.customer_id = c.customer_id
)

SELECT
    customer_state,
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
            COUNT(*) FILTER (WHERE has_complete_delivery_dates),
            0
        ),
        2
    ) AS late_delivery_rate_pct
FROM customer_orders
GROUP BY customer_state
ORDER BY late_delivery_rate_pct DESC;
