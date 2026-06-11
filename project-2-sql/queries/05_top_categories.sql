SELECT
    oi.category,
    SUM(oi.quantity)                            AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS revenue,
    RANK() OVER (ORDER BY SUM(oi.quantity * oi.unit_price) DESC) AS revenue_rank
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id AND o.order_status = 'Completed'
GROUP BY oi.category
ORDER BY revenue DESC;