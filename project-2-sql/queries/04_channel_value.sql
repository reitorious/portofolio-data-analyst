SELECT
    c.channel,
    COUNT(DISTINCT c.customer_id)              AS customers,
    COUNT(DISTINCT o.order_id)                 AS orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    ROUND(SUM(oi.quantity * oi.unit_price) / COUNT(DISTINCT c.customer_id), 2) AS revenue_per_customer
FROM customers c
LEFT JOIN orders o       ON o.customer_id = c.customer_id AND o.order_status = 'Completed'
LEFT JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.channel
ORDER BY revenue DESC;