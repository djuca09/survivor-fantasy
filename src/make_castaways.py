from src.castaway import Castaway
import json
from src.update_points import update_castaway_points


def castaway_lookup(URL : str , szn_num : int) -> dict[str,Castaway]:
    with open (f"data/s{szn_num}/s{szn_num}_castaway_list.json", "r") as castaway_file:
        castaway_names = json.load(castaway_file)

    castaways = [Castaway(name) for name in castaway_names]

    update_castaway_points(URL , castaways)

    return {c.name(): c for c in castaways}


if __name__ == "__main__":
    print(castaway_lookup("https://www.globaltv.com/survivor-47-fantasy-tribe/#results", 47))

