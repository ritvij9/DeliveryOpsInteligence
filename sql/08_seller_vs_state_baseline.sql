
WITH seller_state AS (
    SELECT DISTINCT
        oi.seller_id,
        c.customer_state,
        b.order_id,
        b.is_late_delivery
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
),

state_baseline AS (
    SELECT
        customer_state,
        COUNT(*) AS state_eligible_orders,
        ROUND(
            100.0 * COUNT(*) FILTER (WHERE is_late_delivery)
            / COUNT(*), 2
        ) AS state_late_rate_pct
    FROM (
        SELECT DISTINCT order_id, customer_state, is_late_delivery
        FROM seller_state
    )
    GROUP BY customer_state
),

seller_state_summary AS (
    SELECT
        seller_id,
        customer_state,
        COUNT(*) AS eligible_orders,
        COUNT(*) FILTER (WHERE is_late_delivery) AS late_orders,
        100.0 * COUNT(*) FILTER (WHERE is_late_delivery)
            / COUNT(*) AS seller_state_late_rate_pct
    FROM seller_state
    GROUP BY seller_id, customer_state
    HAVING COUNT(*) >= 50
)

SELECT
    s.seller_id,
    s.customer_state,
    s.eligible_orders,
    s.late_orders,
    ROUND(s.seller_state_late_rate_pct, 2) AS seller_state_late_rate_pct,
    b.state_eligible_orders,
    b.state_late_rate_pct,
    ROUND(
        s.seller_state_late_rate_pct - b.state_late_rate_pct, 2
    ) AS percentage_point_difference
FROM seller_state_summary s
JOIN state_baseline b USING (customer_state)
ORDER BY percentage_point_difference DESC;
