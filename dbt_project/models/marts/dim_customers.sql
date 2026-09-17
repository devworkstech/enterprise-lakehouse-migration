WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),
orders AS (
    SELECT
        customer_id,
        COUNT(order_id) AS lifetime_orders,
        COALESCE(SUM(total_amount), 0) AS lifetime_value
    FROM {{ ref('stg_orders') }}
    WHERE order_status = 'COMPLETED'
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    c.email,
    c.first_name,
    c.last_name,
    COALESCE(o.lifetime_orders, 0) AS lifetime_orders,
    COALESCE(o.lifetime_value, 0.0) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
