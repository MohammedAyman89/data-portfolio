import requests
import pandas as pd
import json
import time

SEARCH_URL = "https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www2.daad.de/deutschland/studienangebote/international-programmes/en/result/"
}

# Parameters for the API request
params = {
    "cert": "",
    "admReq": "",
    "langExamPC": "",
    "scholarshipLC": "",
    "langExamLC": "",
    "scholarshipSC": "",
    "langExamSC": "",
    "degree[]": "1",  # Bachelor's degree
    "fos": "",
    "langDeAvailable": "",
    "langEnAvailable": "",
    "lang[]": "4",  # English
    "fee": "",
    "sort": "4",
    "dur": "",
    "q": "",
    "limit": "100",
    "offset": "0",
    "display": "list",
    "isElearning": "",
    "isSep": ""
}

all_results = []

# Fetch data with pagination
for page in range(0, 5):  # Get 5 pages (offset-based pagination)
    offset = page * 100
    params["offset"] = str(offset)
    
    print(f"Fetching page {page + 1} (offset: {offset})...")
    
    try:
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            continue
        
        data = response.json()
        results = data.get("courses", [])
        
        if not results:
            print("No more results found.")
            break
    
        for item in results:
            all_results.append({
                "program_ID": item.get("id", ""),
                "program_name": item.get("courseNameShort", ""),
                "subject": item.get("subject", ""),
                "city": item.get("city", ""),
                "language": ", ".join(item.get("languages", [])) if isinstance(item.get("languages"), list) else item.get("languages", ""),
                "duration": item.get("programmeDuration", ""),
                "tuition_fee": item.get("tuitionFees", "")
            })
        
        print(f"Found {len(results)} programs on this page.")
        
        # Add delay between requests to be respectful
        time.sleep(1)
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        continue
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
        continue

print(f"\nTotal programs collected: {len(all_results)}")

if all_results:
    # Create DataFrame
    df = pd.DataFrame(all_results)
    print("\nFirst 5 programs:")
    print(df.head())
    
    # Save to CSV
    output_csv = "DAAD-requests.csv"
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    
