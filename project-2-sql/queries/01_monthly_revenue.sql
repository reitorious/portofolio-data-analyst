WITH monthly AS (
    SELECT
        strftime('%Y-%m', o.order_date)            AS month,
        SUM(oi.quantity * oi.unit_price)           AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 2)                                       AS revenue,
    ROUND(SUM(revenue) OVER (ORDER BY month), 2)            AS running_total,
    ROUND(revenue * 100.0 / SUM(revenue) OVER (), 1)        AS pct_of_year
FROM monthly
ORDER BY month;