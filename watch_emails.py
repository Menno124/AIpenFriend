import json
import os

THREAD_FILE = 'thread_tracker.json'

def load_threads():
    if os.path.exists(THREAD_FILE):
        with open(THREAD_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_threads(thread_data):
    with open(THREAD_FILE, 'w') as f:
        json.dump(thread_data, f, indent=2)
