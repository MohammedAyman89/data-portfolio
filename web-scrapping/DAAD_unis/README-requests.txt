# 🎓 DAAD University Programs Scraper

This project scrapes structured university program data from the official DAAD (German Academic Exchange Service) search API for international programs in Germany.

It demonstrates advanced web scraping with:
- Custom headers (browser-like)
- GET requests with complex query parameters
- Pagination using offset
- JSON parsing to structured CSV

---

## ✅ 📌 Project Goals

✔️ Extract real academic program data from DAAD.de  
✔️ Handle realistic API constraints (offset-based pagination)  
✔️ Parse and clean JSON to CSV  
✔️ Produce a dataset ready for analysis or client delivery

---

## 🛠️ Tech Stack

- Python
- requests
- pandas
- time

---

## ✅ Features

⭐ Mimics real browser traffic with custom headers  
⭐ Supports large-scale scraping with offset pagination  
⭐ Handles network errors and JSON decoding errors gracefully  
⭐ Delays requests to avoid rate-limiting or bans  
⭐ Outputs clean UTF-8 CSV

---

## 📂 Output Example (DAAD.csv)

| program_ID | program_name                  | subject         | city     | language | duration | tuition_fee | university                        | degree_type | url                                  |
|------------|------------------------------|-----------------|----------|----------|----------|-------------|-----------------------------------|-------------|--------------------------------------|
| 123456     | Computer Science (MSc)       | Computer Science| Berlin   | English  | 2 years  | €1000/year  | Technical University of Berlin    | 1           | https://www2.daad.de/...             |
| 654321     | Software Engineering (MSc)   | Engineering     | Munich   | English  | 2 years  | €1500/year  | University of Munich              | 1           | https://www2.daad.de/...             |

✅ Supports hundreds/thousands of rows depending on `offset` and `limit`.

---

## 🧭 How it Works

1️⃣ Opens the DAAD search API endpoint:
https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json


2️⃣ Sets realistic headers:
- User-Agent
- Accept
- Referer
- ... etc.

3️⃣ Uses query parameters to filter:
- Degree type (e.g. Bachelor's = 1)
- Language (English only)
- Offset (pagination)

4️⃣ Loops through pages to collect data.

5️⃣ Parses JSON fields like:
- id
- courseNameShort
- programmeDuration
- tuitionFees
- city
- languages

6️⃣ Appends results to a pandas DataFrame.

7️⃣ Saves to CSV with UTF-8 encoding.

---

## 💻 Usage

### Install Requirements
```bash
pip install requests pandas
