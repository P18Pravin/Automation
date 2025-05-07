import requests
import json
import os

# Basic config
BASE_URL = "http://localhost:9200"
AUTH = ("admin", "admin")
OUTPUT_FOLDER = "output"

# Ensure output directory exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Fetch all index names from OpenSearch
def fetch_index_list():
    try:
        res = requests.get(f"{BASE_URL}/_cat/indices?h=index", auth=AUTH, timeout=10)
        res.raise_for_status()
        raw_indices = res.text.strip().split("\n")
        return [name.strip() for name in raw_indices if name]
    except Exception as e:
        print(f"[ERROR] Failed to get indices: {e}")
        return []

# Build monitor structure per index
def create_monitor_entry(index_name, idx):
    return {
        "Monitor_Name": f"{index_name} - Error Check",
        "Index": index_name,
        "Text2Scan_in_Message": "error",
        "Time2Scan": "5m",
        "notification_channel": f"notification_channel_{idx}"
    }

def main():
    index_list = fetch_index_list()
    if not index_list:
        print("No indices found. Exiting.")
        return

    monitors = []
    for count, index in enumerate(index_list, start=1):
        monitor = create_monitor_entry(index, count)
        monitors.append(monitor)

    final_payload = {"Monitors": monitors}
    output_path = os.path.join(OUTPUT_FOLDER, "monitors.json")

    try:
        with open(output_path, "w") as f:
            json.dump(final_payload, f, indent=4)
        print(f"[INFO] Monitor JSON saved to {output_path}")
    except Exception as write_err:
        print(f"[ERROR] Could not write output file: {write_err}")

if __name__ == "__main__":
    main()
