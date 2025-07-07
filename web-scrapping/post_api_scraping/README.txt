# 🎯 University Course Catalog Scraper (POST API)

This project demonstrates **advanced web scraping** using a real university's course catalog search that requires **POST** requests with JSON body, anti-CSRF tokens, and session cookies.

It’s a great example of scraping realistic forms / search endpoints that use POST to deliver data.

---

## ✅ 📌 Project Overview

✔️ Target: Evansville University Course Catalog  
✔️ URL: https://ssb.evansville.edu/Student/Courses  
✔️ Uses anti-CSRF tokens for POST  
✔️ Pagination supported via POST parameters  
✔️ Extracts course information in clean CSV

---

## ✅ 💻 Features

⭐ Sends **initial GET** to fetch session cookies and CSRF token  
⭐ Builds custom **POST** request body with filters  
⭐ Includes anti-CSRF header  
⭐ Handles pagination automatically  
⭐ Parses JSON response  
⭐ Extracts structured fields:
- Course Code
- Course Title
- Credits
- Description

⭐ Saves results to **CSV** for analysis

---

## ✅ 🗺️ Data Source
Evansville University Course Search:

- Initial GET:
https://ssb.evansville.edu/Student/Courses

- POST endpoint:
https://ssb.evansville.edu/Student/Courses/PostSearchCriteria


---

## ✅ 📂 Example Output (courses.csv)

| code    | title                        | credit | description                                                 |
|---------|-----------------------------|--------|-------------------------------------------------------------|
| CSCI 101| Introduction to Computing   | 3      | An overview of computer science concepts and programming.   |
| MATH 201| Calculus I                   | 4      | Limits, derivatives, integrals, and applications.           |

✅ Clean, structured, ready for analysis or client use.

---

## ✅ 🛠️ Requirements

- Python 3.8+
- requests
- pandas
- time

Install dependencies:

```bash
pip install requests pandas

✅ 🏃 How to Run
1️⃣ Make sure your working directory contains the script.

2️⃣ Run:
python evansville_scraper.py
3️⃣ Output:
evansville_courses.csv

✅ ⚙️ How It Works
✔️ Step 1: Sends GET request to Course Catalog page

Retrieves session cookies

Extracts __RequestVerificationToken

✔️ Step 2: Builds POST request

Includes custom headers

Sets JSON body with filters and pagination

✔️ Step 3: Parses JSON response

Extracts course details

Handles multiple pages automatically

✔️ Step 4: Saves structured results as CSV

✅ 🌟 Highlights
⭐ Real-world POST scraping
⭐ Anti-CSRF token handling
⭐ Session cookies management
⭐ Custom headers to simulate browser traffic
⭐ Pagination support
⭐ Clean CSV export

✅ ⚠️ Notes
Be polite: includes download delay to avoid overloading server.

Always check terms of service / robots.txt before scraping production systems.

For demo/portfolio use, limit scraping volume to avoid issues.

✅ 📈 Why This Project
This project is part of my Freelance Data Portfolio showcasing:

✔️ Advanced scraping skills
✔️ Handling POST APIs with JSON bodies
✔️ Managing headers, cookies, and anti-CSRF tokens
✔️ Producing client-ready CSV deliverables

👤 Author
Mohammed Ayman – Freelance Data Specialist


