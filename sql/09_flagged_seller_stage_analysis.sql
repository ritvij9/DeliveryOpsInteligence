
WITH seller_state_orders AS (
    SELECT DISTINCT
        oi.seller_id,
        c.customer_state,
        b.order_id,
        b.is_late_delivery,
        b.purchase_to_delivery_days,
        b.carrier_handoff_ts,
        b.customer_delivery_ts
    FROM read_parquet(
        'data/processed/order_delivery_base.parquet'
    ) b
    JOIN read_csv_auto(
        'data/raw/olist_order_items_dataset.csv'
    ) oi ON b.order_id = oi.order_id
    JOIN read_csv_auto(
        'data/raw/olist_customers_dataset.csv'
    ) c ON b.customer_id = c.customer_id
    WHERE b.has_complete_delivery_dates
),
flagged AS (
    SELECT *
    FROM seller_state_orders
    WHERE
        (seller_id = '88460e8ebdecbfecb5f9601833981930'
            AND customer_state = 'SP')
        OR
        (seller_id = '7d13fca15225358621be4086e1eb0964'
            AND customer_state = 'RJ')
        OR
        (seller_id = '4869f7a5dfa277a7dca6462dcf3b52b2'
            AND customer_state = 'RJ')
        OR
        (seller_id = '4a3ca9315b744ce9f8e9374361493884'
            AND customer_state = 'RS')
)
SELECT
    seller_id,
    customer_state,
    COUNT(*) AS eligible_orders,
    COUNT(*) FILTER (WHERE is_late_delivery) AS late_orders,
    ROUND(
        AVG(
            date_diff(
                'hour', carrier_handoff_ts, customer_delivery_ts
            ) / 24.0
        ), 2
    ) AS avg_carrier_to_customer_days,
    ROUND(
        AVG(
            date_diff(
                'hour', carrier_handoff_ts, customer_delivery_ts
            ) / 24.0
        ) FILTER (WHERE is_late_delivery), 2
    ) AS late_avg_carrier_to_customer_days,
    ROUND(
        AVG(
            date_diff(
                'hour', carrier_handoff_ts, customer_delivery_ts
            ) / 24.0
        ) FILTER (WHERE NOT is_late_delivery), 2
    ) AS ontime_avg_carrier_to_customer_days
FROM flagged
WHERE carrier_handoff_ts IS NOT NULL
  AND customer_delivery_ts IS NOT NULL
GROUP BY seller_id, customer_state
ORDER BY customer_state, late_orders DESC;
