import json
from src.player import Player

def make_players(season_num: int , merge_week : int) -> list[Player]:
    path = f"data/s{season_num}/s{season_num}_players.json"
    try:
        with open(path, 'r') as f:
            player_dicts = json.load(f)
    except FileNotFoundError:
        return []

    players = []
    for p in player_dicts:
        player = Player(
            name=p.get("name"),
            castaway_names=p.get("castaway_names"),
            winner_pick=p.get("winner_pick"),
            merge_pickup=p.get("merge_pickup"),
            merge_drop=p.get("merge_drop"),
            merge_week= merge_week
        )
        players.append(player)

    return players
