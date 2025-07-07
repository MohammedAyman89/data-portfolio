import pandas as pd
import re
from datetime import datetime
import numpy as np

def clean_csv_data(input_file, output_file):
    """
    Clean the CSV data according to specified requirements:
    1. Standardize date formats to DD/MM/YYYY
    2. Clean price and total columns (remove currency symbols)
    3. Remove rows with missing essential data
    4. Ensure quantity is positive integer
    5. Recalculate total = price * quantity
    6. Ensure CSV consistency
    """
    
    # Read the CSV file
    print("Reading CSV file...")
    df = pd.read_csv(input_file)
    print(f"Original data shape: {df.shape}")
    
    # 1. Clean Date Column - Standardize to DD/MM/YYYY format
    print("\nCleaning date formats...")
    def standardize_date(date_str):
        if pd.isna(date_str) or date_str == '':
            return None
        
        date_str = str(date_str).strip()
        
        # Different date patterns to handle
        patterns = [
            # YYYY-MM-DD or YYYY/MM/DD or YYYY.MM.DD
            (r'(\d{4})[./-](\d{1,2})[./-](\d{1,2})', lambda m: f"{m.group(3).zfill(2)}/{m.group(2).zfill(2)}/{m.group(1)}"),
            # DD-MM-YYYY or DD/MM/YYYY or DD.MM.YYYY
            (r'(\d{1,2})[./-](\d{1,2})[./-](\d{4})', lambda m: f"{m.group(1).zfill(2)}/{m.group(2).zfill(2)}/{m.group(3)}"),
            # DD Mon YYYY (e.g., "20 Jan 2024")
            (r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})', 
             lambda m: f"{m.group(1).zfill(2)}/{month_to_num(m.group(2))}/{m.group(3)}"),
        ]
        
        for pattern, formatter in patterns:
            match = re.match(pattern, date_str, re.IGNORECASE)
            if match:
                try:
                    return formatter(match)
                except:
                    continue
        
        return None
    
    def month_to_num(month_str):
        months = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        return months.get(month_str.lower(), '01')
    
    df['purchase_date'] = df['purchase_date'].apply(standardize_date)
    
    # 2. Clean Price and Total Columns - Remove currency symbols
    print("Cleaning price and total columns...")
    def clean_currency(value):
        if pd.isna(value) or value == '':
            return 0
        
        # Convert to string and remove currency symbols and spaces
        value_str = str(value).strip()
        # Remove €, $, and any other non-numeric characters except decimal point and minus
        cleaned = re.sub(r'[^\d.-]', '', value_str)
        
        try:
            return float(cleaned) if cleaned else 0
        except:
            return 0
    
    df['price'] = df['price'].apply(clean_currency)
    df['total'] = df['total'].apply(clean_currency)
    
    # 3. Clean customer_name and item columns
    print("Cleaning customer_name and item columns...")
    df['customer_name'] = df['customer_name'].fillna('').astype(str).str.strip()
    df['item'] = df['item'].fillna('').astype(str).str.strip()
    
    # 4. Clean quantity column - ensure positive integers
    print("Cleaning quantity column...")
    def clean_quantity(qty):
        if pd.isna(qty):
            return 0
        try:
            qty_int = int(float(qty))
            return max(0, qty_int)  # Ensure non-negative
        except:
            return 0
    
    df['quantity'] = df['quantity'].apply(clean_quantity)
    
    # 5. Remove rows with missing essential data
    print("Removing rows with missing essential data...")
    initial_count = len(df)
    
    # Remove rows where essential fields are missing or invalid
    df = df[
        (df['customer_name'] != '') &  # customer_name not empty
        (df['item'] != '') &           # item not empty
        (df['quantity'] > 0) &         # quantity positive
        (df['price'] > 0) &            # price positive
        (df['purchase_date'].notna())  # valid date
    ]
    
    removed_count = initial_count - len(df)
    print(f"Removed {removed_count} rows with missing/invalid essential data")
    
    # 6. Recalculate total = price * quantity
    print("Recalculating totals...")
    df['total'] = df['price'] * df['quantity']
    
    # 7. Reset index and ensure proper data types
    df = df.reset_index(drop=True)
    
    # Round price and total to 2 decimal places
    df['price'] = df['price'].round(2)
    df['total'] = df['total'].round(2)
    
    # Ensure transaction_id is integer
    df['transaction_id'] = df['transaction_id'].astype(int)
    df['quantity'] = df['quantity'].astype(int)
    
    # 8. Save cleaned data
    print(f"\nSaving cleaned data to {output_file}...")
    df.to_csv(output_file, index=False)
    
    print(f"Cleaned data shape: {df.shape}")
    print(f"Removed {removed_count} invalid rows")
    print(f"Final dataset has {len(df)} valid transactions")
    
    # Display sample of cleaned data
    print("\nSample of cleaned data:")
    print(df.head(10).to_string(index=False))
    
    return df

def validate_cleaned_data(df):
    """
    Validate the cleaned data meets all requirements
    """
    print("\n=== VALIDATION REPORT ===")
    
    # Check date format consistency
    date_pattern = r'^\d{2}/\d{2}/\d{4}$'
    invalid_dates = df[~df['purchase_date'].str.match(date_pattern, na=False)]
    print(f"✓ Date format (DD/MM/YYYY): {len(invalid_dates) == 0} - {len(invalid_dates)} invalid dates")
    
    # Check no missing essential data
    missing_customer = df[df['customer_name'] == ''].shape[0]
    missing_item = df[df['item'] == ''].shape[0]
    print(f"✓ No missing customer names: {missing_customer == 0} - {missing_customer} missing")
    print(f"✓ No missing items: {missing_item == 0} - {missing_item} missing")
    
    # Check positive quantities
    negative_qty = df[df['quantity'] <= 0].shape[0]
    print(f"✓ All quantities positive: {negative_qty == 0} - {negative_qty} non-positive")
    
    # Check positive prices
    negative_price = df[df['price'] <= 0].shape[0]
    print(f"✓ All prices positive: {negative_price == 0} - {negative_price} non-positive")
    
    # Check total calculation accuracy
    df['calculated_total'] = df['price'] * df['quantity']
    incorrect_totals = df[abs(df['total'] - df['calculated_total']) > 0.01].shape[0]
    print(f"✓ Correct total calculations: {incorrect_totals == 0} - {incorrect_totals} incorrect")
    
    print("\n=== SUMMARY STATISTICS ===")
    print(f"Total transactions: {len(df)}")
    print(f"Unique customers: {df['customer_name'].nunique()}")
    print(f"Unique items: {df['item'].nunique()}")
    print(f"Date range: {df['purchase_date'].min()} to {df['purchase_date'].max()}")
    print(f"Price range: ${df['price'].min():.2f} to ${df['price'].max():.2f}")
    print(f"Quantity range: {df['quantity'].min()} to {df['quantity'].max()}")
    
if __name__ == "__main__":
    input_file = "before_big.csv"
    output_file = "after_big.csv"
    
    print("=== CSV DATA CLEANING SCRIPT ===")
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    
    try:
        # Clean the data
        cleaned_df = clean_csv_data(input_file, output_file)
        
        # Validate the results
        validate_cleaned_data(cleaned_df)
        
        print("\n✅ Data cleaning completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during data cleaning: {str(e)}")
        import traceback
        traceback.print_exc()

