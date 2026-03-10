import json
import os

def save_manual_points(szn_num: int, castaway_name: str, week: int, delta: int):
    
    path = f"data/s{szn_num}/s{szn_num}_manual_points.json"

    # Load existing or start fresh
    if os.path.exists(path):
        with open(path, "r") as f:
            manual_points = json.load(f)
    else:
        manual_points = {}

    # Update the entry
    if castaway_name not in manual_points:
        manual_points[castaway_name] = {}

    manual_points[castaway_name][str(week)] = delta

    with open(path, "w") as f:
        json.dump(manual_points, f, indent=2)