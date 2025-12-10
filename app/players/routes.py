from app.players import bp
import requests
from flask import request, jsonify
from auth.auth import token_auth
from app.models.player import Player, db,PlayerIn, PlayerOut, PlayerTeamUpdateIn
from app.models.team import Team,TeamIn, TeamOut
from app.models.user import User, UserOut
from app.models.tournament import Tournament, TournamentOut
from config import Config
from app.matchups.api_read import get_api_key
import os


riot_api_key = os.getenv("RIOT_API_KEY")
#riot_api_key = get_api_key('riot_api_key.txt')

# get all players
@bp.get('/')
@bp.auth_required(token_auth)
@bp.output(PlayerOut(many=True))
def get_all_users():
    players = Player.query.all()
    return players

# get player by id
@bp.get('/<int:player_id>')
@bp.auth_required(token_auth)
@bp.output(PlayerOut)
def get_player(player_id):
    return db.get_or_404(Player, player_id)

# get player by name
@bp.get('/<string:summoner_name>')
@bp.auth_required(token_auth)
@bp.output(PlayerOut)
def get_player_by_summoner_name(summoner_name):
    player = Player.query.filter_by(summoner_name=summoner_name).first()
    if not player:
        return jsonify({'message': 'Player not found'}), 404
    return PlayerOut.dump(player), 200

# create player
@bp.post('/')
@bp.auth_required(token_auth)
@bp.input(PlayerIn, location='json')
@bp.output(PlayerOut, status_code=201)
def create_player(json_data):
    summoner_name = json_data['summoner_name']
    tag = json_data['tag']
    puuid = None
    summoner_level = None
    team_id = json_data.get('team_id', None)
    #print("API_KEY:", RIOT_API_KEY)  # Debugging line to check if API key is loaded
    try:
        # === Try to fetch puuid ===
        account_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}?api_key={riot_api_key}"
        #print("Riot Account URL:", account_url)  # Debugging line to check the URL
        headers = {
            "X-Riot-Token": riot_api_key
        }
        #print("Request Headers:", headers)  # Debugging line to check headers
        acc_response = requests.get(account_url)
        #print("Response status:", acc_response.status_code)  # Debugging line to check response status

        if acc_response.status_code == 200:
            puuid = acc_response.json().get("puuid")
            # === Try to fetch summoner level ===
            summoner_url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={riot_api_key}"
            summoner_response = requests.get(summoner_url)

            if summoner_response.status_code == 200:
                summoner_level = summoner_response.json().get("summonerLevel")

    except Exception as e:
        # Optional: log error or print(e)
        #print(f"Error calling Riot API: {e}")
        #print(f"Response content: {getattr(e.response, 'text', '')}")
        pass  # Continue without puuid or level

    # === Create player anyway ===
    player = Player(
        summoner_name=summoner_name,
        tag=tag,
        puuid=puuid,
        summoner_level=summoner_level,
        team_id=team_id
    )
    # Create and save player
    player = Player(**json_data)
    db.session.add(player)
    db.session.commit()

    return player



# Change only the player's team
@bp.put('/<int:player_id>/team')
@bp.auth_required(token_auth)
@bp.input(PlayerTeamUpdateIn, location='json')
@bp.output(PlayerOut, status_code=200)
def update_player_team(player_id, json_data):
    player = Player.query.get_or_404(player_id)
    player.team_id = json_data['team_id']
    db.session.commit()
    return player

# delete player
@bp.delete('/<int:player_id>')
@bp.auth_required(token_auth)
@bp.output({}, status_code=204)
def delete_player(player_id):
    player = db.get_or_404(Player, player_id)
    db.session.delete(player)
    db.session.commit()
    return ''
