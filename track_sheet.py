import os
import json
import pandas as pd

SPREADSHEET_ID = "1FUzAZyTCgFTVxQ--qbCAS2bUk4dsAw6ASxwjURPHbyI"

def fetch_sheet_data():
    all_tracks = []
    
    # We target key tabs using their sheet export endpoints or names
    # GID for 'Fully Leaked' or downloading CSVs of main tabs
    tab_urls = {
        "Fully Leaked": f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Fully%20Leaked",
        "Recent": f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Recent",
        "Unreleased": f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet=Unreleased"
    }
    
    for tab_name, url in tab_urls.items():
        try:
            print(f"Fetching tab: {tab_name}...")
            df = pd.read_csv(url)
            df.columns = [str(c).strip() for c in df.columns]
            
            records = df.to_dict(orient="records")
            for row in records:
                # Filter valid rows that have a song Name and Era
                if any(pd.notna(val) for val in row.values()):
                    clean_row = {k: (str(v) if pd.notna(v) else "") for k, v in row.items()}
                    clean_row["SheetSource"] = tab_name
                    all_tracks.append(clean_row)
        except Exception as e:
            print(f"Error fetching {tab_name}: {e}")

    return all_tracks

def save_sheet_data(data):
    os.makedirs("data", exist_ok=True)
    file_path = "data/google_sheet_tracker.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} total entries to {file_path}")

if __name__ == "__main__":
    tracker_data = fetch_sheet_data()
    save_sheet_data(tracker_data)
