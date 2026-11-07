import os
import json
import pandas as pd

SPREADSHEET_ID = "1FUzAZyTCgFTVxQ--qbCAS2bUk4dsAw6ASxwjURPHbyI"

TABS = [
    "Unreleased",
    "Fully Leaked",
    "Recent",
    "Snippets/Partials",
    "Grails",
    "File Dates",
    "OG Files (Unreleased)",
    "OG Files (Released)"
]

def fetch_sheet_data():
    all_tracks = []
    
    for tab in TABS:
        encoded_tab = tab.replace(" ", "%20").replace("/", "%2F")
        url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"
        
        try:
            print(f"Fetching tab: {tab}...")
            df = pd.read_csv(url, header=None) # Load raw to handle custom sheet headers
            
            # Find the actual header row dynamically (contains 'Era' or 'Name')
            header_row_idx = None
            for idx, row in df.iterrows():
                row_str = " ".join([str(val) for val in row.values])
                if "Era" in row_str and "Name" in row_str:
                    header_row_idx = idx
                    break

            if header_row_idx is not None:
                df.columns = df.iloc[header_row_idx]
                df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
                df.columns = [str(c).strip() for c in df.columns]

                for _, row in df.iterrows():
                    name = str(row.get("Name", "")).strip()
                    era = str(row.get("Era", "")).strip()
                    
                    # Ignore blank or banner rows
                    if name and name.lower() != "nan" and "total" not in era.lower():
                        clean_row = {}
                        for col in df.columns:
                            val = str(row.get(col, "")).strip()
                            clean_row[col] = val if val.lower() != "nan" else ""
                        clean_row["SheetSource"] = tab
                        all_tracks.append(clean_row)
        except Exception as e:
            print(f"Error reading tab {tab}: {e}")

    return all_tracks

def save_sheet_data(data):
    os.makedirs("data", exist_ok=True)
    file_path = "data/google_sheet_tracker.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} total track records to {file_path}")

if __name__ == "__main__":
    tracker_data = fetch_sheet_data()
    save_sheet_data(tracker_data)
