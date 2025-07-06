# File: utils.py

def get_top_senders(df):
    """
    Returns the two most frequent senders.
    Pads with 'Unknown' if less than 2 are found.
    """
    senders = df['sender'].value_counts().index.tolist()
    if len(senders) >= 2:
        return senders[0], senders[1]
    elif len(senders) == 1:
        return senders[0], "Unknown"
    else:
        return "Unknown", "Unknown"
