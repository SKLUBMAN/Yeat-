import os
import json
import pandas as pd

SPREADSHEET_ID = "1FUzAZyTCgFTVxQ--qbCAS2bUk4dsAw6ASxwjURPHbyI"

TABS = [
    "Unreleased",
    "Released",
    "Recent",
    "Best Of",
    "Snippets/Partials",
    "Grails",
    "OG Files (Unreleased)",
    "OG Files (Released)",
    "File Dates",
    "Misc"
]

def fetch_sheet_data():
    all_tracks = []
    
    for tab in TABS:
        encoded_tab = tab.replace(" ", "%20").replace("/", "%2F")
        url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"
        
        try:
            print(f"Fetching category: {tab}...")
            df = pd.read_csv(url, header=None)
            
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
                    
                    if name and name.lower() != "nan" and "total" not in era.lower() and name != "Name":
                        clean_row = {}
                        for col in df.columns:
                            val = str(row.get(col, "")).strip()
                            clean_row[col] = val if val.lower() != "nan" else ""
                        
                        clean_row["Category"] = tab
                        clean_row["Era"] = era if era else "Other / Misc"
                        all_tracks.append(clean_row)
        except Exception as e:
            print(f"Error reading {tab}: {e}")

    return all_tracks

def save_sheet_data(data):
    os.makedirs("data", exist_ok=True)
    with open("data/google_sheet_tracker.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} track records")

if __name__ == "__main__":
    save_sheet_data(fetch_sheet_data())
