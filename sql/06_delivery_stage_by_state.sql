
WITH order_stages AS (
    SELECT
        b.order_id,
        b.is_late_delivery,
        c.customer_state,
        CASE
            WHEN b.carrier_handoff_ts IS NOT NULL
             AND b.customer_delivery_ts >= b.carrier_handoff_ts
            THEN DATE_DIFF(
                'hour',
                b.carrier_handoff_ts,
                b.customer_delivery_ts
            ) / 24.0
        END AS carrier_to_customer_days
    FROM read_parquet(
        'data/processed/order_delivery_base.parquet'
    ) b
    JOIN read_csv_auto(
        'data/raw/olist_customers_dataset.csv'
    ) c
        ON b.customer_id = c.customer_id
    WHERE b.has_complete_delivery_dates
)

SELECT
    customer_state,
    COUNT(*) AS eligible_orders,
    COUNT(*) FILTER (WHERE is_late_delivery) AS late_orders,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE is_late_delivery)
        / COUNT(*), 2
    ) AS late_rate_pct,
    ROUND(
        AVG(carrier_to_customer_days)
        FILTER (WHERE is_late_delivery), 2
    ) AS late_avg_carrier_to_customer_days,
    ROUND(
        AVG(carrier_to_customer_days)
        FILTER (WHERE NOT is_late_delivery), 2
    ) AS ontime_avg_carrier_to_customer_days
FROM order_stages
GROUP BY customer_state
HAVING COUNT(*) >= 500
ORDER BY late_rate_pct DESC;
