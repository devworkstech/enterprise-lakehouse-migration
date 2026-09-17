SELECT
    CAST(order_id AS BIGINT) AS order_id,
    CAST(customer_id AS BIGINT) AS customer_id,
    CAST(order_date AS TIMESTAMP) AS order_date,
    CAST(total_amount AS DECIMAL(18,2)) AS total_amount,
    UPPER(TRIM(status)) AS order_status
FROM {{ source('bronze', 'raw_orders') }}
WHERE order_id IS NOT NULL
