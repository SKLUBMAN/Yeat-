import os
import json
import pandas as pd

# The public Google Sheet ID from your link
SPREADSHEET_ID = "1FUzAZyTCgFTVxQ--qbCAS2bUk4dsAw6ASxwjURPHbyI"
# Export URL as CSV
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv"

def fetch_sheet_data():
    try:
        print("Fetching data from Yeat Tracker Google Sheet...")
        df = pd.read_csv(CSV_URL)
        
        # Clean column headers
        df.columns = [str(c).strip() for c in df.columns]
        
        # Convert dataframe to dictionary records
        records = df.to_dict(orient="records")
        
        # Filter out completely empty or header noise rows
        cleaned_records = []
        for row in records:
            # Keep rows that have valid track/era information
            if any(pd.notna(val) for val in row.values()):
                # Convert NaN to empty string for JSON serialization
                clean_row = {k: (v if pd.notna(v) else "") for k, v in row.items()}
                cleaned_records.append(clean_row)

        return cleaned_records
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return []

def save_sheet_data(data):
    os.makedirs("data", exist_ok=True)
    file_path = "data/google_sheet_tracker.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved {len(data)} entries from Google Sheet to {file_path}")

if __name__ == "__main__":
    tracker_data = fetch_sheet_data()
    save_sheet_data(tracker_data)
                            
