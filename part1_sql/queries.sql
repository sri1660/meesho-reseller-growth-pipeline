CREATE TABLE IF NOT EXISTS dummy(id INTEGER);

--------------------------------------------------------
-- 1. Monthly Revenue by Category
--------------------------------------------------------
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price),2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;

--------------------------------------------------------
-- 2. Region-wise Revenue and Orders
--------------------------------------------------------
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price),2) AS total_revenue,
    COUNT(o.order_id) AS total_orders
FROM orders o
JOIN resellers r
ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;

--------------------------------------------------------
-- 3. Top 5 Resellers (Spend > 50000)
--------------------------------------------------------
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price),2) AS total_spend
FROM orders o
JOIN resellers r
ON o.reseller_id = r.reseller_id
GROUP BY r.reseller_id
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;

--------------------------------------------------------
-- 4A. Resellers with No Orders
--------------------------------------------------------
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers r
LEFT JOIN orders o
ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;

--------------------------------------------------------
-- 4B. COUNT(*) vs COUNT(order_id)
--------------------------------------------------------
SELECT
    r.reseller_id,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
ON r.reseller_id = o.reseller_id
WHERE r.reseller_id='RS024'
GROUP BY r.reseller_id;

--------------------------------------------------------
-- 5. June Delivered Average Order Value
--------------------------------------------------------
SELECT
    ROUND(
        SUM(quantity * unit_price) / COUNT(*),
        2
    ) AS june_aov
FROM orders
WHERE month='June'
AND status='Delivered';