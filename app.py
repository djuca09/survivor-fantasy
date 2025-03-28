from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
from src.make_castaways import castaway_lookup
import json
from src.make_players import make_players

app = Flask(__name__)

app.secret_key = 'Barry-Allen'

#Load site settings from JSON
settings_path = "data/site_settings.json"
with open(settings_path, 'r') as f:
    settings = json.load(f)

season = settings["season"]
points_url = settings["points_url"]
merge_week = settings["merge_week"]

#Initialize globals
castaway_dict = castaway_lookup(points_url,season)
players = make_players(season , merge_week)
castaway_names = list(castaway_dict.keys())
players_path = f"data/s{season}/s{season}_players.json"

def load_players_file(): #load players file
    try:
        with open(players_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def write_players_file(new_players): #write changes to players file and update players list in code
    with open(players_path, 'w') as f:
        json.dump(new_players, f, indent=2)
    global players
    players = make_players(season, merge_week) #Update players

######################################################################################

@app.route('/')
def home():
    sorted_players = sorted(players, key=lambda p: p.points(castaway_dict), reverse=True)
    return render_template('index.html', players = sorted_players , castaway_dict = castaway_dict, season = season)


@app.route('/edit_players')
def edit_players():    
    return render_template('edit_players.html', players=players , castaway_names = castaway_names)

@app.route('/delete_player', methods=['POST'])
def delete_player():
    
    player_name = request.form.get('player_name')

    #load file, filter out player, and save
    new_players = load_players_file()
    new_players = [p for p in new_players if p.get("name") != player_name]
    write_players_file(new_players)

    return redirect('/edit_players')

@app.route('/create_player', methods=['GET'])
def create_player():
    return render_template('create_player.html', castaway_names=castaway_names)

@app.route('/submit_player', methods=['POST'])
def submit_player():
    # Capture the player's name
    name = request.form['player_name']

    # Capture all selected castaways (it's a multi-select, so it's a list)
    selected_castaway_names = request.form.getlist('castaways')

    # Capture the winner pick (single select)
    winner = request.form['winner']

    # Optional merge values
    merge_pickup = request.form.get('merge_pick') or None
    merge_drop = request.form.get('merge_drop') or None
    merge_week = request.form.get('merge_week') or None

    #Prepare a dict version of the player for JSON
    player_data = {
        "name": name,
        "castaway_names": selected_castaway_names,
        "winner_pick": winner
    }

    # Add optional merge data if provided
    if merge_pickup:
        player_data["merge_pickup"] = merge_pickup
    if merge_drop:
        player_data["merge_drop"] = merge_drop
    if merge_week:
        player_data["merge_week"] = int(merge_week)

    #load file, add player, and save
    new_players = load_players_file()
    new_players.append(player_data)
    write_players_file(new_players)

    return render_template('player_added.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html', season = season, points_url = points_url, merge_week = merge_week)

@app.route('/update_settings', methods=['POST'])
def update_settings():

    global season,points_url,merge_week,castaway_dict,players,castaway_names,players_path

    season = request.form.get('season') or season
    points_url = request.form.get('points_url') or points_url

    #Make sure it's a string
    merge_week_input = request.form.get('merge_week')
    merge_week = int(merge_week_input) if merge_week_input else merge_week


    # Save to site_settings.json
    settings = {
        "season": season,
        "points_url": points_url,
        "merge_week": int(merge_week)
    }

    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)

    castaway_dict = castaway_lookup(points_url,season)
    players = make_players(season , merge_week)
    castaway_names = list(castaway_dict.keys())
    players_path = f"data/s{season}/s{season}_players.json"

    return render_template('settings_updated.html')

@app.route('/edit_merge_pickup', methods=['POST'])
def edit_merge_pickup():

    merge_pick = request.form.get("merge_pick")
    player_name = request.form.get("player_name")

    #load file, update merge pickup, and save
    new_players = load_players_file()
    for p in new_players:
       if p.get("name") == player_name:
           p["merge_pickup"] = merge_pick  
    write_players_file(new_players)

    flash(f"Merge pick updated!", category=f"{player_name} pickup")
    return redirect('/edit_players')

@app.route('/edit_merge_drop', methods=['POST'])
def edit_merge_drop():

    merge_drop = request.form.get("merge_drop")
    player_name = request.form.get("player_name")

    #load file, update merge pickup, and save
    new_players = load_players_file()
    for p in new_players:
       if p.get("name") == player_name:
           p["merge_drop"] = merge_drop  
    write_players_file(new_players)

    flash(f"Merge drop updated!", category=f"{player_name} drop")
    return redirect('/edit_players')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'dostet daram Elaha':  # replace with real one
            return redirect('/admin')
        else:
            flash('Incorrect password')
            return redirect('/admin_login')
    return render_template('admin_login.html')

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

app.run()
