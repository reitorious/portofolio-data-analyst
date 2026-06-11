WITH first_order AS (   -- bulan pertama tiap pelanggan order (cohort-nya)
    SELECT customer_id, MIN(strftime('%Y-%m', order_date)) AS cohort_month
    FROM orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
),
activity AS (           -- bulan-bulan di mana pelanggan aktif order
    SELECT DISTINCT customer_id, strftime('%Y-%m', order_date) AS active_month
    FROM orders
    WHERE order_status = 'Completed'
)
SELECT
    f.cohort_month,
    a.active_month,
    COUNT(DISTINCT a.customer_id) AS active_customers
FROM first_order f
JOIN activity a ON a.customer_id = f.customer_id
WHERE a.active_month >= f.cohort_month
GROUP BY f.cohort_month, a.active_month
ORDER BY f.cohort_month, a.active_month;