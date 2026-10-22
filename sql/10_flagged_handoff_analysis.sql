
WITH order_seller_state AS (
    SELECT DISTINCT
        oi.seller_id,
        c.customer_state,
        b.order_id,
        b.is_late_delivery,
        b.approved_ts,
        b.carrier_handoff_ts
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
state_handoff AS (
    SELECT
        customer_state,
        COUNT(*) AS state_orders,
        AVG(date_diff('hour', approved_ts, carrier_handoff_ts) / 24.0)
            AS state_avg_handoff_days
    FROM (
        SELECT DISTINCT
            customer_state, order_id, approved_ts, carrier_handoff_ts
        FROM order_seller_state
    )
    WHERE approved_ts IS NOT NULL
      AND carrier_handoff_ts IS NOT NULL
    GROUP BY customer_state
),
seller_handoff AS (
    SELECT
        seller_id,
        customer_state,
        COUNT(*) AS eligible_orders,
        COUNT(*) FILTER (WHERE is_late_delivery) AS late_orders,
        AVG(date_diff('hour', approved_ts, carrier_handoff_ts) / 24.0)
            AS avg_handoff_days
    FROM order_seller_state
    WHERE approved_ts IS NOT NULL
      AND carrier_handoff_ts IS NOT NULL
    GROUP BY seller_id, customer_state
    HAVING COUNT(*) >= 50
)
SELECT
    s.seller_id,
    s.customer_state,
    s.eligible_orders,
    s.late_orders,
    ROUND(s.avg_handoff_days, 2) AS seller_avg_handoff_days,
    ROUND(b.state_avg_handoff_days, 2) AS state_avg_handoff_days,
    ROUND(s.avg_handoff_days - b.state_avg_handoff_days, 2)
        AS difference_days
FROM seller_handoff s
JOIN state_handoff b USING (customer_state)
WHERE
    (s.seller_id = '88460e8ebdecbfecb5f9601833981930'
        AND s.customer_state = 'SP')
    OR
    (s.seller_id = '7d13fca15225358621be4086e1eb0964'
        AND s.customer_state = 'RJ')
    OR
    (s.seller_id = '4869f7a5dfa277a7dca6462dcf3b52b2'
        AND s.customer_state = 'RJ')
    OR
    (s.seller_id = '4a3ca9315b744ce9f8e9374361493884'
        AND s.customer_state = 'RS')
ORDER BY difference_days DESC;
