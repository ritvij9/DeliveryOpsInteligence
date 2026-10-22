
-- DeliveryOps Intelligence
-- Purpose: Compare delivery-stage durations for late and on-time orders.
-- This analysis identifies associations, not proven causes.

WITH stage_durations AS (
    SELECT
        order_id,
        is_late_delivery,
        purchase_ts,
        approved_ts,
        carrier_handoff_ts,
        customer_delivery_ts,

        CASE
            WHEN approved_ts >= purchase_ts
            THEN DATE_DIFF('hour', purchase_ts, approved_ts) / 24.0
        END AS purchase_to_approval_days,

        CASE
            WHEN carrier_handoff_ts >= approved_ts
            THEN DATE_DIFF(
                'hour', approved_ts, carrier_handoff_ts
            ) / 24.0
        END AS approval_to_carrier_days,

        CASE
            WHEN customer_delivery_ts >= carrier_handoff_ts
            THEN DATE_DIFF(
                'hour', carrier_handoff_ts, customer_delivery_ts
            ) / 24.0
        END AS carrier_to_customer_days,

        DATE_DIFF(
            'hour', purchase_ts, customer_delivery_ts
        ) / 24.0 AS total_transit_days

    FROM read_parquet(
        'data/processed/order_delivery_base.parquet'
    )
    WHERE has_complete_delivery_dates
)

SELECT
    CASE
        WHEN is_late_delivery THEN 'Late'
        ELSE 'On time'
    END AS delivery_group,

    COUNT(*) AS eligible_orders,

    COUNT(purchase_to_approval_days) AS approval_stage_orders,
    ROUND(AVG(purchase_to_approval_days), 2) AS avg_approval_days,
    ROUND(MEDIAN(purchase_to_approval_days), 2) AS median_approval_days,

    COUNT(approval_to_carrier_days) AS handoff_stage_orders,
    ROUND(AVG(approval_to_carrier_days), 2) AS avg_approval_to_carrier_days,
    ROUND(MEDIAN(approval_to_carrier_days), 2) AS median_approval_to_carrier_days,

    COUNT(carrier_to_customer_days) AS delivery_stage_orders,
    ROUND(AVG(carrier_to_customer_days), 2) AS avg_carrier_to_customer_days,
    ROUND(MEDIAN(carrier_to_customer_days), 2) AS median_carrier_to_customer_days,

    ROUND(AVG(total_transit_days), 2) AS avg_total_transit_days,
    ROUND(MEDIAN(total_transit_days), 2) AS median_total_transit_days

FROM stage_durations
GROUP BY delivery_group
ORDER BY delivery_group;
