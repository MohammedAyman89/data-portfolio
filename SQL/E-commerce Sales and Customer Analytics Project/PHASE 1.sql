CREATE DATABASE IF NOT EXISTS olist_ecommerce_db;
-- phase1 
-- task1: Quarterly Performance

SELECT 
    CONCAT('Q',
            QUARTER(o.order_purchase_timestamp),
            ' ',
            YEAR(o.order_purchase_timestamp)) AS quarter_field,
    SUM(i.price + i.freight_value) AS Total_Revenue,
    COUNT(DISTINCT o.order_id) AS Total_Orders,
    (SUM(i.price + i.freight_value) / COUNT(DISTINCT o.order_id)) AS average_order_value	
FROM 
    orders o
        JOIN
    order_items i ON o.order_id = i.order_id
GROUP BY quarter_field
;


-- task2: Sales Channel Analysis
WITH PaymentMetrics AS(
	SELECT 
		payment_type,
		SUM(payment_value) AS revenue,
		AVG(payment_installments) AS avg_installment_count,
		AVG(payment_value) AS avg_payment_value
	FROM
		order_payments
	GROUP BY payment_type
	),
TotalRevenue As (
	SELECT SUM(revenue) AS GrandTotal FROM PaymentMetrics)
    SELECT 
		pm.payment_type,
        pm.revenue,
        (pm.revenue / tr.GrandTotal) * 100 AS revenue_share_percent,
        pm.avg_installment_count,
        pm.avg_payment_value
    FROM PaymentMetrics pm, TotalRevenue tr
	ORDER BY 
		revenue DESC
	LIMIT 3;

-- task 3: Top Product Movers
SELECT 
    tr.product_category_name_english AS Product_Category,
    COUNT(i.product_id) AS Total_Items_Sold
FROM
    order_items i
        JOIN
    products p ON i.product_id = p.product_id
        JOIN
    product_category_name_translation tr ON p.product_category_name = tr.product_category_name
GROUP BY Product_Category
ORDER BY Total_Items_Sold DESC
LIMIT 10;

-- TASK 4: Geographic Revenue
SELECT 
    s.seller_state,
    SUM(i.price + i.freight_value) AS Total_Revenue,
    AVG(i.freight_value) AS avg_freight_value,
    COUNT(DISTINCT c.customer_unique_id) AS Total_Customers_served
FROM
    order_items i
        JOIN
    sellers s ON i.seller_id = s.seller_id
        JOIN
    orders o ON i.order_id = o.order_id
        JOIN
    customers c ON o.customer_id = c.customer_id
GROUP BY s.seller_state
ORDER BY Total_Revenue DESC
LIMIT 5;

    
    

