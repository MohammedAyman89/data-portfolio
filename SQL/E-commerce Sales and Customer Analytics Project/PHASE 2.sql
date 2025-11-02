USE olist_ecommerce_db; 
-- task 5: Order Delivery Lag
SELECT
	-- Use YYYY-MM for chronological sorting (hidden from final SELECT)
    DATE_FORMAT(order_delivered_customer_date, '%Y-%m') AS sort_key,
    AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)) AS average_delivery_speed,
    AVG(DATEDIFF(order_estimated_delivery_date, order_purchase_timestamp)) AS average_promised_delivery
FROM 
	orders
WHERE
	order_status = 'delivered' 
    AND order_delivered_customer_date IS NOT NULL
GROUP BY sort_key
ORDER BY sort_key;

-- task 6: Cumulative Revenue
-- solution 1
WITH monthly_revenue AS(
	SELECT
	DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS per_date,
    SUM(i.price + i.freight_value) AS sales_month
FROM
	orders o
		JOIN
	order_items i ON o.order_id = i.order_id
WHERE 
	o.order_status = 'delivered'
GROUP BY per_date
)
SELECT 
	per_date,
    sales_month,
    SUM(sales_month) OVER (ORDER BY per_date) AS running_total
FROM
	monthly_revenue;
    
-- solution 2

SELECT 
	DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS per_date,
    SUM(i.price + i.freight_value) AS sales_month,
    SUM(SUM(i.price + i.freight_value)) OVER (ORDER BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')) AS running_total
FROM
	orders o
		JOIN
	order_items i ON o.order_id = i.order_id
WHERE 
	o.order_status = 'delivered'
GROUP BY per_date;

-- task 7: Best Performing Sellers

SELECT * FROM sellers;
SELECT * FROM order_items;
SELECT * FROM orders;
WITH seller_data AS(
SELECT 
	seller_id,
    COUNT(order_id) AS Total_Orders_Fulfilled
FROM 
	order_items
GROUP BY seller_id
)
SELECT
	RANK() OVER(ORDER BY Total_Orders_Fulfilled DESC) AS Seller_Rank,
    seller_id,
    Total_Orders_Fulfilled
FROM
	seller_data
LIMIT 10;
    
