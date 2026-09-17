SELECT
    DATE(order_date) AS revenue_date,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS gross_revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM {{ ref('stg_orders') }}
WHERE order_status = 'COMPLETED'
GROUP BY DATE(order_date)
