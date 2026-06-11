CREATE VIEW v_completed_revenue AS
SELECT
    o.order_id,
    o.order_date,
    c.channel,
    r.restaurant_name,
    r.city,
    oi.category,
    oi.quantity * oi.unit_price AS line_revenue
FROM orders o
JOIN customers c    ON c.customer_id = o.customer_id
JOIN restaurants r  ON r.restaurant_id = o.restaurant_id
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed';

-- contoh pakai: revenue per kota jadi sangat singkat
SELECT city, ROUND(SUM(line_revenue), 2) AS revenue
FROM v_completed_revenue
GROUP BY city
ORDER BY revenue DESC;