import pandas as pd
import glob

# كل ملفات المبيعات في فولدر
csv_files = glob.glob("sales_data/sales_*.csv")

print("Merging files:", csv_files)

all_data = []
for file in csv_files:
    df = pd.read_csv(file)
    all_data.append(df)

merged_df = pd.concat(all_data, ignore_index=True)
print("✅ Merged Shape:", merged_df.shape)

merged_df.to_csv("all_sales.csv", index=False)

df = pd.read_csv("all_sales.csv")

# 1. استخراج العملة من price
df['currency'] = df['price'].str.extract(r'([€$])')
df['price_clean'] = df['price'].str.replace(r'[^\d.-]', '', regex=True).astype(float)

# 2. استخراج العملة من total
df['total_clean'] = df['total'].str.replace(r'[^\d.-]', '', regex=True).astype(float)

# 3. فلترة معاملات قيمتها عالية (>500)
high_value = df[df['total_clean'] > 500]

high_value.to_csv("high_value_sales.csv", index=False)
print("✅ High-value transactions saved.")

df['discounted_price'] = df['price_clean'] * 0.9
df['discounted_total'] = df['discounted_price'] * df['quantity']

df.to_csv("all_sales_with_discounts.csv", index=False)
print("✅ Discounts applied and saved.")

summary = df.groupby('product').agg(
    total_quantity = ('quantity', 'sum'),
    total_sales = ('total_clean', 'sum')
).reset_index()

summary.to_csv("sales_summary.csv", index=False)
print("✅ Sales summary saved.")
