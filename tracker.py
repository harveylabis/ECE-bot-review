"""TRACKS WHICH FILE IS ALREADY SENT TO AVOID DUPLICATION

author: pororomero
created: 07/18/2021
"""

import json
from datetime import datetime

log = {}
filename = "log_counter.json"

def read_counter(filename=filename):
    with open(filename, 'r', encoding="utf8") as f:
        logs = json.load(f)
    log.update(logs)
    print("Reading ID for the current session...")
    current_id = len(logs)
    print("Current ID:", current_id)
    print()

    return current_id

def write_counter(id):
    now = datetime.now()
    now_str_form = now.strftime("%d/%m/%Y %H:%M:%S") 
    log_data = f"{id} was successfully sent at {now_str_form}"
    log[id] = log_data

    with open(filename, 'w', encoding="utf8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print()
    print("Writing ID for the next send...")

    return None
