"# Graphs and Charts"  

# File: visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")

def plot_message_frequency(df):
    df['date'] = df['timestamp'].dt.date
    freq = df.groupby('date').size()

    plt.figure(figsize=(10, 4))
    freq.plot(kind='line', color='dodgerblue')
    plt.title("Messages Per Day")
    plt.xlabel("Date")
    plt.ylabel("Number of Messages")
    plt.tight_layout()
    return plt

def plot_sender_distribution(df):
    sender_counts = df['sender'].value_counts()

    plt.figure(figsize=(6, 6))
    sender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
    plt.title("Message Share")
    plt.ylabel("")
    plt.tight_layout()
    return plt

def plot_reply_time_distribution(reply_times_sec):
    mins = [r / 60 for r in reply_times_sec if r < 3600]

    plt.figure(figsize=(8, 4))
    sns.histplot(mins, bins=20, kde=True, color='orchid')
    plt.title("Reply Time Distribution")
    plt.xlabel("Reply Time (minutes)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    return plt
