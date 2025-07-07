# 📌 CSV Data Cleaning Project

This project demonstrates professional-level data cleaning for a messy e-commerce transaction dataset using Python.

---

## ✅ Project Overview

The dataset simulates customer transactions with fields like:

- transaction_id
- customer_name
- purchase_date
- item
- quantity
- price
- total

The raw (before) CSV contains:
✔️ Inconsistent date formats
✔️ Currency symbols in price and total
✔️ Missing or invalid entries
✔️ Wrong total calculations

Our cleaning script standardizes, validates, and fixes these issues automatically.

---

## ✅ Files in This Folder

- **before_big.csv**  
  The raw messy data file with ~1000 rows.

- **after.csv**  
  The cleaned, processed output.

- **cleaning_script.py**  
  Python script that performs all cleaning steps.

- **README.txt**  
  This documentation file.

---

## ✅ Cleaning Steps Performed

1️⃣ **Standardize Dates**  
   - Convert all dates to `DD/MM/YYYY`.
   - Handle various formats: `YYYY-MM-DD`, `DD Mon YYYY`, etc.

2️⃣ **Clean Price and Total Columns**  
   - Remove currency symbols (€,$).
   - Convert to floats.

3️⃣ **Remove Invalid Rows**  
   - Drop rows with missing customer_name, item, date.
   - Ensure quantity and price are positive.

4️⃣ **Recalculate Total**  
   - total = price * quantity.

5️⃣ **Output Clean CSV**  
   - Save cleaned data to `after.csv`.

---

## ✅ How to Run

### Requirements
- Python 3.x
- pandas
- faker (for generating sample data)

### Install dependencies
```bash
pip install pandas faker
