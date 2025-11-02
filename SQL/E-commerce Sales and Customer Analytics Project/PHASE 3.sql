-- task 8: RFM Calculation
CREATE VIEW RFM_reuirenments AS 
SELECT 
    c.customer_unique_id,
    DATEDIFF((SELECT 
                    MAX(order_purchase_timestamp)
                FROM
                    orders),
            MAX(o.order_purchase_timestamp)) AS Recency_days,
	COUNT(o.order_id) AS frequent_payments,
    SUM(p.payment_value) AS Payment_Values
FROM
    customers c
        JOIN
    orders o ON c.customer_id = o.customer_id
		JOIN
	order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_unique_id
;
SELECT * FROM RFM_reuirenments;
-- task 9: RFM Scoring
DROP VIEW RFM_rates;
CREATE VIEW RFM_rates AS
SELECT 
	customer_unique_id,
	NTILE(5) OVER (ORDER BY Recency_days DESC) AS Recency_Rate,
    NTILE(5) OVER (ORDER BY frequent_payments) AS frequent_rate,
    NTILE(5) OVER (ORDER BY Payment_Values) AS Payment_Rate
FROM
	RFM_reuirenments;

SELECT * FROM RFM_rates;

-- TASK 10: Customer Classification

SELECT
	customer_unique_id,
    Recency_Rate,
    frequent_rate,
    Payment_rate,
    CASE
		WHEN Recency_Rate >= 4 AND frequent_rate >= 4 AND Payment_Rate >= 4 THEN '1. Champion'
        WHEN Recency_Rate >= 3 AND frequent_rate >= 4 AND Payment_Rate >= 3 THEN '2. Loyal Customers'
        WHEN Recency_Rate = 5 AND frequent_rate = 1 AND Payment_Rate = 1 THEN '3. New Customers'
        WHEN Recency_Rate <= 2 AND frequent_rate <= 2 AND Payment_Rate <= 2 THEN '4. At Risk'
        ELSE '5. Needs Attention'
	END AS Customer_Segment
FROM
	RFM_rates
ORDER BY Customer_Segment, Recency_Rate DESC;
    


