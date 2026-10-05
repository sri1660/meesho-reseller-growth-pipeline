import sqlite3
import pandas as pd
import os

DB_PATH = "../data/meesho_reseller.db"
OUT = "output"

os.makedirs(OUT, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

queries = {
    "monthly_category_revenue.csv": """
        SELECT month, category,
        ROUND(SUM(quantity*unit_price),2) AS revenue,
        COUNT(*) AS n_orders
        FROM orders
        GROUP BY month, category
        ORDER BY
        CASE month
            WHEN 'April' THEN 1
            WHEN 'May' THEN 2
            WHEN 'June' THEN 3
        END, category;
    """,

    "region_revenue.csv": """
        SELECT r.region,
        ROUND(SUM(o.quantity*o.unit_price),2) AS total_revenue,
        COUNT(o.order_id) AS total_orders
        FROM orders o
        JOIN resellers r
        ON o.reseller_id=r.reseller_id
        GROUP BY r.region;
    """,

    "top_resellers.csv": """
        SELECT r.reseller_id,
        r.reseller_name,
        ROUND(SUM(o.quantity*o.unit_price),2) AS total_spend
        FROM orders o
        JOIN resellers r
        ON o.reseller_id=r.reseller_id
        GROUP BY r.reseller_id
        HAVING total_spend>50000
        ORDER BY total_spend DESC
        LIMIT 5;
    """,

    "inactive_resellers.csv": """
        SELECT r.reseller_id,
        r.reseller_name,
        r.region
        FROM resellers r
        LEFT JOIN orders o
        ON r.reseller_id=o.reseller_id
        WHERE o.order_id IS NULL;
    """,

    "left_join_count_demo.csv": """
        SELECT
        r.reseller_id,
        COUNT(*) AS count_star,
        COUNT(o.order_id) AS count_order_id
        FROM resellers r
        LEFT JOIN orders o
        ON r.reseller_id=o.reseller_id
        WHERE r.reseller_id='RS024'
        GROUP BY r.reseller_id;
    """,

    "june_aov.csv": """
        SELECT ROUND(
        SUM(quantity*unit_price)/COUNT(*),2
        ) AS june_aov
        FROM orders
        WHERE month='June'
        AND status='Delivered';
    """
}

for filename, sql in queries.items():
    df = pd.read_sql_query(sql, conn)
    df.to_csv(os.path.join(OUT, filename), index=False)
    print(f"Saved {filename}")

conn.close()
print("All SQL outputs generated successfully.")
