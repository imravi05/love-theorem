"# Prediction Logic"  
# File: predictor.py

import pandas as pd
import numpy as np

def compute_metrics(df, user_name, crush_name):
    """
    Computes reply time, frequency, and conversation duration between user and crush.

    Parameters:
    - df: DataFrame with parsed WhatsApp messages
    - user_name: your name as it appears in the chat
    - crush_name: the other person's name

    Returns: dict of metrics
    """
    # Sort by time
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Filter out only messages between user and crush
    df = df[(df['sender'] == user_name) | (df['sender'] == crush_name)]

    reply_times = []
    last_user_msg_time = None

    for i, row in df.iterrows():
        if row['sender'] == user_name:
            last_user_msg_time = row['timestamp']
        elif row['sender'] == crush_name and last_user_msg_time:
            # Calculate reply time
            delta = (row['timestamp'] - last_user_msg_time).total_seconds()
            if 5 < delta < 60 * 60 * 6:  # ignore unrealistic or delayed replies
                reply_times.append(delta)
            last_user_msg_time = None

    # Average reply time (in minutes)
    avg_reply_min = np.mean(reply_times) / 60 if reply_times else 999

    # Frequency: messages per day
    df['date'] = df['timestamp'].dt.date
    messages_per_day = df.groupby('date').size()
    avg_messages_per_day = messages_per_day.mean()

    # Conversation duration = max consecutive back & forth messages in a single day
    conversation_lengths = []
    current_len = 1
    last_sender = df.iloc[0]['sender']

    for sender in df['sender'][1:]:
        if sender != last_sender:
            current_len += 1
        else:
            conversation_lengths.append(current_len)
            current_len = 1
        last_sender = sender
    conversation_lengths.append(current_len)
    avg_convo_length = np.mean(conversation_lengths)

    return {
        'avg_reply_time_min': round(avg_reply_min, 2),
        'avg_messages_per_day': round(avg_messages_per_day, 2),
        'avg_convo_length': round(avg_convo_length, 2)
    }

def calculate_interest_score(metrics):
    """
    Calculates interest score out of 100 based on weighted formula.

    Lower reply time, higher frequency, and longer conversation = higher score.
    """
    # Normalize using simple min-max scaling based on assumptions
    rt = max(0, min(1, (60 - metrics['avg_reply_time_min']) / 60))  # best at 0 min, worst at 60+
    freq = min(metrics['avg_messages_per_day'] / 50, 1)  # 50+ msgs/day = max
    convo = min(metrics['avg_convo_length'] / 10, 1)  # 10+ turns per convo = max

    # Weighted score
    score = (0.4 * rt + 0.3 * freq + 0.3 * convo) * 100
    return round(score, 2)
