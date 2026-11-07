import os
import json
import requests
from bs4 import BeautifulSoup

# Direct URL targeting Yeat thread results on leaked.cx
LEAKED_CX_URL = "https://leaked.cx/forums/hip-hop/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_recently_surfaced():
    response = requests.get(LEAKED_CX_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to reach target. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    surfaced_leaks = []

    # Parse XenForo thread list
    threads = soup.select(".structItem--thread")
    for thread in threads:
        title_element = thread.select_one(".structItem-title a")
        time_element = thread.select_one("time")
        
        if title_element:
            title = title_element.get_text(strip=True)
            link = "https://leaked.cx" + title_element.get("href", "")
            date = time_element.get("datetime") if time_element else "Unknown"

            # Filter exclusively for Yeat content
            if "yeat" in title.lower():
                surfaced_leaks.append({
                    "title": title,
                    "url": link,
                    "date_surfaced": date,
                    "source": "leaked.cx"
                })

    return surfaced_leaks

def save_data(data):
    os.makedirs("data", exist_ok=True)
    file_path = "data/recently_surfaced.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} items to {file_path}")

if __name__ == "__main__":
    leaks = fetch_recently_surfaced()
    save_data(leaks)
