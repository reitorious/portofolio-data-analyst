WITH resto_rev AS (
    SELECT
        r.city,
        r.restaurant_name,
        SUM(oi.quantity * oi.unit_price) AS revenue
    FROM restaurants r
    JOIN orders o       ON o.restaurant_id = r.restaurant_id AND o.order_status = 'Completed'
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY r.restaurant_id
)
SELECT city, restaurant_name, ROUND(revenue, 2) AS revenue, rnk
FROM (
    SELECT
        city, restaurant_name, revenue,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC) AS rnk
    FROM resto_rev
)
WHERE rnk <= 3
ORDER BY city, rnk;