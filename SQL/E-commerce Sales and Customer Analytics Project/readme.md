# 🛍️ E-commerce Sales and Customer Analytics Project

## 🎯 Project Overview

This project involves a comprehensive **SQL data analysis** of a large Brazilian e-commerce public dataset (Olist). The goal was to transform raw transactional data into **actionable business intelligence (BI)** across three core areas: Foundational Reporting, Advanced Time-Series Analysis, and Customer Segmentation.

The entire analysis was performed using advanced SQL techniques, including **Window Functions, CTEs, and Conditional Aggregation.**

---

## ⚙️ Technical Stack

* **Primary Tool:** **SQL** (e.g., MySQL)
* **Database:** Olist E-commerce Dataset (9 tables including orders, customers, sellers, products, and reviews).
* **Key Skills Demonstrated:**
    * **Advanced SQL:** CTEs, Views, `NTILE()`, `RANK()`, `SUM() OVER()`, `DATEDIFF()`.
    * **Data Modeling:** Complex multi-table joins (4+ table joins).
    * **BI & Reporting:** KPI calculation (AOV, Revenue), Time-Series Analysis.
    * **Data Science:** RFM Segmentation, Sentiment Classification.

---

## 🔑 Key Analytical Phases & Insights

The project was structured into three phases, plus a bonus sentiment analysis section:

### I. Foundational Reporting (Operational KPIs)
* **Quarterly Performance:** Demonstrated **strong year-over-year revenue growth** from 2017 to 2018.
* **Sales Channels:** Identified **Credit Card** as the dominant payment type.
* **Product Performance:** Identified **'Bed\_Bath\_Table'** and **'Health\_Beauty'** as top-selling categories by volume.
* **Geographic Hubs:** Confirmed **São Paulo (SP)** as the overwhelmingly dominant hub for sellers and transactions.

### II. Advanced Analytics (Time-Series & Ranking)
* **Delivery Performance:** Quantified the difference between **average actual delivery speed** and **average estimated delivery time** by month.
* **Cumulative Revenue:** Calculated the **running total revenue** across the dataset's lifespan using the `SUM() OVER (ORDER BY...)` Window Function.
* **Seller Ranking:** Ranked all sellers by order fulfillment volume using the **`RANK()`** Window Function to identify the **Top 10 Performers**.

### III. Customer Segmentation (RFM)
* **RFM Scoring:** Applied the **`NTILE(5)`** Window Function to assign scores (1-5) for Recency, Frequency, and Monetary value to every unique customer.
* **Classification:** Used **`CASE` statements** to categorize customers into strategic groups: **'Champions'**, **'Loyal Customers'**, **'New Customers'**, and **'At Risk'**.

### IV. Bonus: Review Sentiment Analysis
* **Distribution:** Calculated the full count of **Score 1 through 5 reviews** per product category to quantify product quality.
* **Classification:** Classified every review score into a qualitative **Sentiment Category** ('Positive', 'Neutral', 'Negative').

---

## 💻 Example SQL Showcase

### 1. **RFM Scoring (NTILE)**
*A demonstration of segmentation and Window Functions.*

```sql
WITH Raw_RFM AS (...) -- Raw R, F, M calculation
SELECT
    customer_unique_id,
    NTILE(5) OVER (ORDER BY Recency_days DESC) AS R_Score,
    NTILE(5) OVER (ORDER BY frequent_payments ASC) AS F_Score,
    NTILE(5) OVER (ORDER BY Payment_Values ASC) AS M_Score
FROM
    Raw_RFM;


### 2. **Running Total (Cumulative Revenue)** 
*A demonstration of time-series analysis.*

``'sql'
WITH Monthly_Sales AS (...) -- Monthly Revenue calculation
SELECT
    per_date,
    sales_month,
    SUM(sales_month) OVER (ORDER BY per_date) AS running_total
FROM
    Monthly_Sales;