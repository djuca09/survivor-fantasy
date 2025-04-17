from flask import jsonify
def build_league_data(castaway_dict,sorted_players,season):


    data = {
        'season': season,
        'players': [],
        'castaways': {
            name: castaway.get_total_points()  # Assuming castaway_dict[name] is a Castaway object with `.points`
            for name, castaway in castaway_dict.items()
        }
    }

    # For determing place
    last_points = None
    last_place = 0
    actual_place = 0

    # Find lowest point total (for last place detection)
    lowest_points = sorted_players[-1].points(castaway_dict)

    for player in sorted_players:
        actual_place += 1
        points = player.points(castaway_dict)

        if points == lowest_points:
            placement = 0
        elif points != last_points:
            last_place = actual_place
            placement = last_place
        else:
            placement = last_place

        last_points = points

        data['players'].append({
        'name': player.name(),
        'points': points,
        'place': placement,
        'castaways': player.castaways(),
        'winner_pick': player.winner_pick(),
        'merge_pickup': player.merge_pickup(),
        'merge_drop': player.merge_drop()
    })

    return jsonify(data)