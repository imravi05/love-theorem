# File: chat_parser.py

import re
from datetime import datetime
import pandas as pd

def parse_chat(file_obj):
    """
    Parses a WhatsApp .txt chat file and returns a DataFrame
    with columns: ['timestamp', 'sender', 'message']
    """
    chat_data = []

    # Updated pattern for your format (handles \u202f)
    pattern = re.compile(
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})[\u202f\s]?([APap][Mm])\s*-\s([^:]+):\s(.*)'
    )

    content = file_obj.read().decode('utf-8', errors='ignore')
    lines = content.splitlines()

    current_msg = ""
    current_sender = None
    current_time = None

    for line in lines:
        line = line.strip()
        match = pattern.match(line)

        if match:
            # Save previous message
            if current_msg and current_sender and current_time:
                chat_data.append([current_time, current_sender, current_msg.strip()])

            date_str, time_str, ampm, sender, message = match.groups()
            time_str_clean = f"{time_str} {ampm}"

            try:
                timestamp = datetime.strptime(f"{date_str} {time_str_clean}", "%d/%m/%y %I:%M %p")
            except ValueError:
                timestamp = None

            current_time = timestamp
            current_sender = sender
            current_msg = message
        else:
            current_msg += ' ' + line

    # Save the last message
    if current_msg and current_sender and current_time:
        chat_data.append([current_time, current_sender, current_msg.strip()])

    # Create DataFrame
    df = pd.DataFrame(chat_data, columns=["timestamp", "sender", "message"])
    df = df.dropna(subset=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df
