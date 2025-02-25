''' Converts Facebook json files from Messenger to a table-formatted HTML file '''

import pandas
import json
import sys
from datetime import datetime

def convert_timestamp(ts):
    try:
        ts_val = float(ts)
    except Exception:
        return ts  # Return as-is if conversion fails
    # Assume timestamps > 1e10 are in milliseconds
    if ts_val > 1e10:
        return datetime.fromtimestamp(ts_val / 1000).strftime("%Y-%m-%d %H:%M:%S")
    else:
        return datetime.fromtimestamp(ts_val).strftime("%Y-%m-%d %H:%M:%S")

# Catch errors in file entry and print usage
if len(sys.argv) < 2:
    print("Usage: python3 panda.py <json_file>")
    sys.exit(1)

json_file = sys.argv[1]

try:
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    messages = data.get("messages", [])
    if not messages:
        print("No messages found in the JSON file.")
        sys.exit(1)

    df = pandas.DataFrame(messages)

    # Convert timestamp to human-readable date
    if "timestamp_ms" in df.columns:
        df["timestamp"] = df["timestamp_ms"].apply(lambda x: datetime.fromtimestamp(x / 1000).strftime("%Y-%m-%d %H:%M:%S"))
        df.drop(columns=["timestamp_ms"], inplace=True)
    elif "timestamp" in df.columns:
        df["timestamp"] = df["timestamp"].apply(convert_timestamp)
    else:
        print("No timestamp column found.")
        sys.exit(1)

    # Remove isUnsent column if present
    if "isUnsent" in df.columns:
        df.drop(columns=["isUnsent"], inplace=True)

    # Rename columns for readability
    if "timestamp" in df.columns:
        df.rename(columns={"timestamp": "Date"}, inplace=True)
    if "senderName" in df.columns:
        df.rename(columns={"senderName": "Sender"}, inplace=True)
    if "text" in df.columns:
        df.rename(columns={"text": "Message"}, inplace=True)
    if "reactions" in df.columns:
        df.rename(columns={"reactions": "Reactions"}, inplace=True)
    if "media" in df.columns:
        df.rename(columns={"media": "Media"}, inplace=True)

    # Reorder columns: Date, Sender, Message, Reactions, Media
    desired_order = [col for col in ["Date", "Sender", "Message", "Reactions", "Media"] if col in df.columns]
    df = df[desired_order]

    output_file = json_file.replace(".json", ".html")
    df.to_html(output_file, escape=False, index=False)

    print(f"HTML file created: {output_file}")

except Exception as e:
    print(f"Error processing file: {e}")

