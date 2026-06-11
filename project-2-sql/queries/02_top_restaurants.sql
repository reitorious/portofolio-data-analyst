SELECT
    r.restaurant_name,
    r.cuisine,
    r.city,
    COUNT(DISTINCT o.order_id)                  AS total_orders,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)  AS revenue
FROM restaurants r
JOIN orders o       ON o.restaurant_id = r.restaurant_id AND o.order_status = 'Completed'
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY r.restaurant_id
ORDER BY revenue DESC
LIMIT 10;