import pandas as pd
import random
import os
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Create output directory
output_dir = "sales_data"
os.makedirs(output_dir, exist_ok=True)

# Define sample products
products = ["Laptop", "Phone", "Tablet", "Headphones", "Monitor", "Keyboard", "Mouse"]
currencies = ["€", "$"]

# Function to generate a single month's sales data
def generate_monthly_sales(month_name, num_rows):
    data = []
    for i in range(1, num_rows + 1):
        customer = fake.name()
        product = random.choice(products)
        quantity = random.randint(1, 5)
        price_value = round(random.uniform(50, 2000), 2)
        currency = random.choice(currencies)
        price = f"{currency} {price_value}"
        total = f"{currency} {round(price_value * quantity, 2)}"
        # Generate date for the specific month
        if month_name == "jan":
            start_date = datetime(2024, 1, 1)
            end_date = datetime(2024, 1, 31)
        elif month_name == "feb":
            start_date = datetime(2024, 2, 1)
            end_date = datetime(2024, 2, 29)
        else:  # mar
            start_date = datetime(2024, 3, 1)
            end_date = datetime(2024, 3, 31)
        
        # Generate random date within the month
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)
        purchase_date = (start_date + timedelta(days=random_days)).strftime("%d/%m/%Y")
        data.append([i, customer, product, quantity, price, total, purchase_date])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=["transaction_id", "customer_name", "product", "quantity", "price", "total", "purchase_date"])
    
    # Save to CSV
    filename = os.path.join(output_dir, f"sales_{month_name}.csv")
    df.to_csv(filename, index=False)
    return filename

# Generate 3 large files (each with 50,000+ rows)
files_created = []
for month, rows in zip(["jan", "feb", "mar"], [50000, 75000, 100000]):
    print(f"Generating {month} sales data with {rows} rows...")
    file = generate_monthly_sales(month, rows)
    files_created.append(file)
    print(f"✅ Created: {file}")

print(f"\n🎉 Successfully created {len(files_created)} large CSV files:")
for file in files_created:
    print(f"  - {file}")

files_created
