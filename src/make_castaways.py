import json
import os
from src.update_points import update_castaway_points
from src.castaway import Castaway


def castaway_lookup(URL : str , szn_num : int) -> dict[str,Castaway]:
    with open (f"data/s{szn_num}/s{szn_num}_castaway_list.json", "r") as castaway_file:
        castaway_names = json.load(castaway_file)

    castaways = [Castaway(name) for name in castaway_names]

    update_castaway_points(URL , castaways)

    # Apply manual point adjustments if file exists
    manual_path = f"data/s{szn_num}/s{szn_num}_manual_points.json"
    if os.path.exists(manual_path):
        with open(manual_path, "r") as f:
            manual_points = json.load(f)

        for castaway in castaways:
            if castaway.name() in manual_points:
                for week_str, delta in manual_points[castaway.name()].items():
                    week = int(week_str)
                    current = castaway.get_weekly_points(week)
                    castaway.set_weekly_points(week, current + delta)

    return {c.name(): c for c in castaways}