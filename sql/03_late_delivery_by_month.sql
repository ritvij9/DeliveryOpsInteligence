
-- DeliveryOps Intelligence
-- Question: How does late-delivery performance vary by purchase month?
-- Grain: One row per purchase month.
-- Denominator: Orders with actual and estimated delivery timestamps.

SELECT
    DATE_TRUNC('month', purchase_ts)::DATE AS purchase_month,
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
    ) AS late_delivery_rate_pct,
    ROUND(
        AVG(purchase_to_delivery_days)
            FILTER (WHERE has_complete_delivery_dates),
        2
    ) AS avg_purchase_to_delivery_days
FROM read_parquet('data/processed/order_delivery_base.parquet')
GROUP BY 1
ORDER BY 1;
