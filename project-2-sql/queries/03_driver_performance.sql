SELECT
    d.driver_name,
    d.vehicle_type,
    COUNT(o.order_id)                  AS deliveries,
    ROUND(AVG(o.delivery_minutes), 1)  AS avg_delivery_min,
    ROUND(AVG(rt.delivery_rating), 2)  AS avg_rating
FROM drivers d
JOIN orders o        ON o.driver_id = d.driver_id AND o.order_status = 'Completed'
LEFT JOIN ratings rt ON rt.order_id = o.order_id
GROUP BY d.driver_id
HAVING deliveries >= 20
ORDER BY avg_rating DESC, avg_delivery_min ASC
LIMIT 10;