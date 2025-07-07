# 🎯 DAAD University Programs Scraper (Scrapy)

This project is a professional **Scrapy spider** for scraping international university programs from the official DAAD.de API. It shows **real-world API scraping** with custom headers, JSON parsing, and CSV export.

---

## 🚀 Features

✅ Uses Scrapy framework for powerful, production-grade crawling  
✅ Custom realistic browser headers and cookies  
✅ GET requests with complex parameters  
✅ Handles JSON API responses  
✅ Extracts multiple program fields into structured CSV  
✅ Includes polite scraping with download delay  
✅ CSV export via Scrapy FEEDS

---

## 🗺️ Data Source

**DAAD (German Academic Exchange Service) International Programmes Search API**  

- Example API Endpoint:
https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json

- Filtered for:
  - Bachelor's degree (degree[]=1)
  - English language (lang[]=4)

---

## 🧾 Extracted Fields

✔️ program_ID  
✔️ name (courseNameShort)  
✔️ subject  
✔️ city  
✔️ language(s)  
✔️ duration  
✔️ fees  

---

## 📂 Example Output (DAAD.csv)

| program_ID | name                          | subject         | city     | language  | duration | fees        |
|------------|------------------------------|-----------------|----------|-----------|----------|-------------|
| 123456     | Computer Science (BSc)       | Computer Science| Berlin   | English   | 3 years  | €1,000/year |
| 654321     | Mechanical Engineering (BSc) | Engineering     | Munich   | English   | 3 years  | €1,500/year |

---

## ⚙️ Project Structure

DAAD-scrapy-version.py/
DAAD-scrapy.csv/
README-scrapy/

---

## 🛠️ Requirements

- Python 3.8+
- Scrapy

Install Scrapy if needed:

```bash
pip install scrapy

how to run:
python daad_spider.py

✅ It will:

Send GET requests with custom headers

Parse JSON responses

Collect fields

Save the structured data to DAAD.csv automatically

💡 How It Works
✔️ Uses Scrapy's request/response pipeline
✔️ Sets realistic browser headers and cookies
✔️ Parses JSON via response.json()
✔️ Extracts desired fields
✔️ Exports to CSV using Scrapy's FEEDS

✅ Highlights of the Code
User-Agent and headers mimic a real browser

Handles API GET params (degree type, language, offset)

Can be expanded for pagination easily

Clean CSV output ready for analysis

🌟 Why Use Scrapy Here?
✅ Designed for large-scale scraping
✅ Built-in throttling and delays
✅ Easy header and cookie management
✅ Auto CSV export via FEEDS
✅ Great for production-quality scrapers

⚠️ Ethical Note
Always respect the website’s terms of service and robots.txt.

Use polite scraping: delays, user-agent rotation, etc.

This project includes a download delay and static headers to avoid overloading the server.

👤 Author
Mohammed Ayman Aly - Freelance Data & Web Scraping Specialist

