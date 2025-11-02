-- Task 11: Score Distribution
SELECT * FROM order_review;
SELECT * FROM order_items;
SELECT * FROM products;
SELECT *  FROM product_category_name_translation;

SELECT
	tr.product_category_name_english,
    COUNT(r.review_score) AS Total_Reviews,
	AVG(r.review_score) AS Avg_Review_Score,
    SUM(CASE WHEN r.review_score = 5 THEN 1 ELSE 0 END) AS Score_5_Count,
    SUM(CASE WHEN r.review_score = 4 THEN 1 ELSE 0 END) AS Score_4_Count,
    SUM(CASE WHEN r.review_score = 3 THEN 1 ELSE 0 END) AS Score_3_Count,
    SUM(CASE WHEN r.review_score = 2 THEN 1 ELSE 0 END) AS Score_2_Count,
    SUM(CASE WHEN r.review_score = 1 THEN 1 ELSE 0 END) AS Score_1_Count
FROM
	order_review r
		JOIN
	order_items i ON r.order_id = i.order_id
		JOIN
	products p ON i.product_id = p.product_id
		JOIN
	product_category_name_translation tr ON p.product_category_name = tr.product_category_name
GROUP BY tr.product_category_name_english
ORDER BY Avg_Review_Score DESC, Total_Reviews DESC;

-- Task 12: Sentiment Classification
SELECT 
	review_id,
    review_score,
    CASE
		WHEN review_score = 5 OR review_score = 4 THEN 'Positive'
        WHEN review_score = 3 THEN 'Neutral'
        WHEN review_score = 1 OR review_score = 2 THEN 'Negative'
	END AS Review_Sentiment
FROM
	order_review;
    