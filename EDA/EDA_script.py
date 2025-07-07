# 📌 Sales Data EDA Full Script

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setup style
sns.set(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)

# 1️⃣ Load data
print("\n✅ Loading data...")
df = pd.read_csv("all_sales_with_discounts.csv")
print(df.head())

# 2️⃣ Quick cleaning check
print("\n✅ Checking columns...")
if 'price' in df.columns:
    df['price_clean'] = df['price'].str.replace(r'[^\d.-]', '', regex=True).astype(float)
if 'total' in df.columns:
    df['total_clean'] = df['total'].str.replace(r'[^\d.-]', '', regex=True).astype(float)

# Show info
print("\n✅ Data Info:")
print(df.info())

# 3️⃣ Descriptive statistics
print("\n✅ Descriptive Statistics:")
print(df.describe())

# 4️⃣ Currency usage
print("\n✅ Currency distribution:")
if 'currency' in df.columns:
    print(df['currency'].value_counts())

# 5️⃣ Total Transactions
print("\n✅ Total Transactions:", len(df))

# 6️⃣ Sales by Product
print("\n✅ Sales by Product:")
product_sales = df.groupby('product')['total_clean'].sum().sort_values(ascending=False)
print(product_sales)

# 📊 Barplot - Total Sales by Product
plt.figure()
sns.barplot(x=product_sales.index, y=product_sales.values)
plt.title("Total Sales by Product")
plt.ylabel("Total Sales (€/$)")
plt.xlabel("Product")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("product_sales_barplot.png")
plt.show()

# 7️⃣ Top 10 Customers
print("\n✅ Top 10 Customers by Total Sales:")
top_customers = df.groupby('customer_name')['total_clean'].sum().sort_values(ascending=False).head(10)
print(top_customers)

# 📊 Horizontal barplot
plt.figure()
top_customers.plot(kind='barh', color='orange')
plt.title("Top 10 Customers by Total Sales")
plt.xlabel("Total Sales (€/$)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top_customers_barplot.png")
plt.show()

# 8️⃣ Price Distribution
plt.figure()
sns.histplot(df['price_clean'], bins=30, kde=True)
plt.title("Price Distribution")
plt.xlabel("Price")
plt.tight_layout()
plt.savefig("price_distribution_hist.png")
plt.show()

# 9️⃣ Quantity Distribution
plt.figure()
sns.histplot(df['quantity'], bins=10, kde=False)
plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.tight_layout()
plt.savefig("quantity_distribution_hist.png")
plt.show()

# 10️⃣ Outlier Detection - Price
plt.figure()
sns.boxplot(x=df['price_clean'])
plt.title("Price Outlier Detection")
plt.tight_layout()
plt.savefig("price_outlier_boxplot.png")
plt.show()

# 11️⃣ Outlier Detection - Quantity
plt.figure()
sns.boxplot(x=df['quantity'])
plt.title("Quantity Outlier Detection")
plt.tight_layout()
plt.savefig("quantity_outlier_boxplot.png")
plt.show()

# 12️⃣ Price vs Quantity Scatterplot
plt.figure()
sns.scatterplot(x='price_clean', y='quantity', data=df, hue='product')
plt.title("Price vs Quantity")
plt.xlabel("Price")
plt.ylabel("Quantity")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("price_vs_quantity_scatter.png")
plt.show()

# 13️⃣ Summary Table
summary_table = df.groupby('product').agg(
    total_quantity=('quantity', 'sum'),
    total_sales=('total_clean', 'sum'),
    avg_price=('price_clean', 'mean')
).reset_index()

print("\n✅ Product Summary Table:")
print(summary_table)

# Save summary table
summary_table.to_csv("product_summary_table.csv", index=False)
print("\n✅ Saved summary table as 'product_summary_table.csv'")

# 14️⃣ Finish
print("\n✅ EDA complete! All charts saved as PNG files.")


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Create output folder (if not exists)
import os
output_folder = "analysis_outputs"
os.makedirs(output_folder, exist_ok=True)

# Example: Save price histogram
plt.figure(figsize=(8, 5))
sns.histplot(df['price_clean'], bins=30, kde=True, color='skyblue')
plt.title("Price Distribution")
plt.xlabel("Price (€/$)")
plt.ylabel("Count")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{output_folder}/price_histogram.png")
plt.close()

# Example: Save quantity histogram
plt.figure(figsize=(8, 5))
sns.histplot(df['quantity'], bins=10, kde=False, color='lightgreen')
plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Count")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{output_folder}/quantity_histogram.png")
plt.close()

# Example: Save price boxplot
plt.figure(figsize=(10, 4))
sns.boxplot(x=df['price_clean'], color='lightblue')
plt.title("Price Outlier Detection")
plt.xlabel("Price (€/$)")
plt.tight_layout()
plt.savefig(f"{output_folder}/price_boxplot.png")
plt.close()

# Example: Save quantity boxplot
plt.figure(figsize=(10, 4))
sns.boxplot(x=df['quantity'], color='lightgreen')
plt.title("Quantity Outlier Detection")
plt.xlabel("Quantity")
plt.tight_layout()
plt.savefig(f"{output_folder}/quantity_boxplot.png")
plt.close()

# 6 Quiantity vs price
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x='price_clean', 
    y='quantity', 
    data=df,
    hue='product',               # Add color by 'product'
    palette='Set2',              # Choose color palette
    s=80,                        # Size of points
    edgecolor='black'            # Optional: black border
)
plt.title("Price vs Quantity")
plt.xlabel("Price (€/$)")
plt.ylabel("Quantity")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Product')
plt.tight_layout()
plt.savefig(f"{output_folder}/price_vs_quantity_boxplot.png")
plt.close()

# Example: Grouped summary table for customers
customer_summary = df.groupby('customer_name')['total_clean'].sum().reset_index().sort_values(by='total_clean', ascending=False)
customer_summary.to_csv(f"{output_folder}/customer_summary.csv", index=False)

# Example: Grouped summary table for products
product_summary = df.groupby('product')['total_clean'].sum().reset_index().sort_values(by='total_clean', ascending=False)
product_summary.to_csv(f"{output_folder}/product_summary.csv", index=False)

print("✅ All plots and summary CSVs saved in 'analysis_outputs' folder!")
