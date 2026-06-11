WITH per_customer AS (
    SELECT
        c.customer_id,
        COUNT(o.order_id) AS orders
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.order_status = 'Completed'
    GROUP BY c.customer_id
)
SELECT
    CASE
        WHEN orders = 0 THEN '0 - belum pernah order'
        WHEN orders = 1 THEN '1 - sekali (one-time)'
        WHEN orders BETWEEN 2 AND 5 THEN '2-5 - repeat'
        ELSE '6+ - loyal'
    END AS segment,
    COUNT(*)                                            AS customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1)  AS pct
FROM per_customer
GROUP BY segment
ORDER BY MIN(orders);