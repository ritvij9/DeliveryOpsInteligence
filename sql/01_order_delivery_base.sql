
-- DeliveryOps Intelligence
-- Purpose: Build a one-row-per-order analytical base.
-- Source: Olist orders CSV.
-- No source rows are deleted; quality issues are flagged.

WITH orders AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        CAST(order_purchase_timestamp AS TIMESTAMP) AS purchase_ts,
        CAST(order_approved_at AS TIMESTAMP) AS approved_ts,
        CAST(order_delivered_carrier_date AS TIMESTAMP) AS carrier_handoff_ts,
        CAST(order_delivered_customer_date AS TIMESTAMP) AS customer_delivery_ts,
        CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_delivery_ts
    FROM read_csv_auto('data/raw/olist_orders_dataset.csv')
),

flagged AS (
    SELECT
        *,
        customer_delivery_ts IS NOT NULL
            AND estimated_delivery_ts IS NOT NULL
            AS has_complete_delivery_dates,

        customer_delivery_ts IS NOT NULL
            AND estimated_delivery_ts IS NOT NULL
            AND customer_delivery_ts > estimated_delivery_ts
            AS is_late_delivery,

        carrier_handoff_ts IS NOT NULL
            AND carrier_handoff_ts < purchase_ts
            AS carrier_before_purchase,

        customer_delivery_ts IS NOT NULL
            AND carrier_handoff_ts IS NOT NULL
            AND customer_delivery_ts < carrier_handoff_ts
            AS delivery_before_carrier,

        order_status = 'delivered'
            AND customer_delivery_ts IS NULL
            AS delivered_missing_actual_timestamp
    FROM orders
)

SELECT
    *,
    CASE
        WHEN has_complete_delivery_dates
        THEN DATE_DIFF(
            'hour',
            purchase_ts,
            customer_delivery_ts
        ) / 24.0
        ELSE NULL
    END AS purchase_to_delivery_days,

    CASE
        WHEN has_complete_delivery_dates
        THEN DATE_DIFF(
            'hour',
            estimated_delivery_ts,
            customer_delivery_ts
        ) / 24.0
        ELSE NULL
    END AS days_late_vs_estimate

FROM flagged;
