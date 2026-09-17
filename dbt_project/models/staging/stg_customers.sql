WITH raw AS (
    SELECT
        CAST(customer_id AS BIGINT) AS customer_id,
        LOWER(TRIM(email)) AS email,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        CAST(created_at AS TIMESTAMP) AS created_at,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY created_at DESC) as rn
    FROM {{ source('bronze', 'raw_customers') }}
)
SELECT customer_id, email, first_name, last_name, created_at
FROM raw WHERE rn = 1
