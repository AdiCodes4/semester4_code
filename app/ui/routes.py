import email
import http
import os
from flask import Blueprint, request, render_template, session, flash, redirect, url_for, current_app
from app.models.user import User, UserIn, LoginIn, UserOut
from app.models.player import Player, PlayerIn, PlayerOut
from app.models.matchup import Matchup
from app.models.tournament import Tournament, TournamentTeam
from app.models.team import Team
from app.ui import bp
from app.users.routes import login_user
import requests
import random
from app.extensions import db
from auth.auth_service import authenticate_user
from app.matchups.api_read import get_api_key
import os
import requests
#from dotenv import load_dotenv



#load_dotenv()  # Load .env into os.environ
API_BASE = 'http://localhost:5000/'
riot_api_key = os.getenv('RIOT_API_KEY')


@bp.route('/')
def index():
    token = session.get('auth_token')
    user_id = session.get('user_id')
    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))

    tournaments = Tournament.query.all()
    teams = Team.query.all()
    players = Player.query.all()
    return render_template('index.html', tournaments=tournaments, teams=teams, players=players)

@bp.route('/create', methods=['GET', 'POST'])
def create_tournament():
    token = session.get('auth_token')
    user_id = session.get('user_id')
    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))
    
    if request.method == 'POST':
        name = request.form['name']
        tournament = Tournament(name=name)
        db.session.add(tournament)
        db.session.commit()

        #create_randomized_matchups(tournament.id)
        return redirect(url_for('ui.manage_tournament_teams', tournament_id=tournament.id))
    return render_template('create_tournament.html')

@bp.route('/tournaments/create_bracket', methods=['POST'])
def create_bracket():
    tournament_id = request.form.get('tournament_id')
    if not tournament_id:
        flash("Tournament ID is required", "error")
        return redirect(url_for('ui.index'))
    tournament = Tournament.query.get_or_404(tournament_id)
    if not tournament.teams:
        flash("No teams assigned to this tournament", "warning")
        return redirect(url_for('ui.view_bracket', tournament_id=tournament.id))

    # Create matchups
    create_randomized_matchups(tournament.id)
    flash("Bracket created successfully!", "success")
    return redirect(url_for('ui.view_bracket', tournament_id=tournament.id))

@bp.route('/bracket/<int:tournament_id>')
def view_bracket(tournament_id):
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))
    
    tournament = Tournament.query.get_or_404(tournament_id)
    matchups = Matchup.query.filter_by(tournament_id=tournament_id).all()
    return render_template('bracket.html', tournament=tournament, matchups=matchups)

@bp.route("/tournaments/<int:tournament_id>/bracket")
def view_brackets(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    teams = [tt.team for tt in tournament.teams]
    return render_template("tournament_bracket.html", tournament=tournament, teams=teams)

def create_randomized_matchups(tournament_id):
    #teams = Team.query.all()
    tournament = Tournament.query.get_or_404(tournament_id) 
    #team_ids = [team.id for team in teams]
    team_ids = [tt.team_id for tt in tournament.teams]
    random.shuffle(team_ids)

    matchups = []
    while len(team_ids) >= 2:
        t1, t2 = team_ids.pop(), team_ids.pop()
        matchups.append(Matchup(tournament_id=tournament_id, team1_id=t1, team2_id=t2))

    if team_ids:
        t1 = team_ids.pop()
        matchups.append(Matchup(tournament_id=tournament_id, team1_id=t1, team2_id=None))

    db.session.add_all(matchups)
    db.session.commit()



#@login_required
@bp.route('/create_player', methods=['GET', 'POST'])
def create_player():
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))

    teams = Team.query.all()
    #print("API_KEY:", RIOT_API_KEY)  # Debugging line to check if API key is loaded

    if request.method == 'POST':
        name = request.form['name']
        tag = request.form['tag']
        team_id = request.form['team_id']

        puuid = None
        summoner_level = None

        try:
            # === Try to fetch puuid ===
            account_url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={riot_api_key}"
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
            pass  # Continue without puuid or level

        # === Create player anyway ===
        player = Player(
            summoner_name=name,
            tag=tag,
            puuid=puuid,
            summoner_level=summoner_level,
            team_id=team_id
        )
        db.session.add(player)
        db.session.commit()

        flash('Spieler erfolgreich hinzugefügt!', "success")
        return redirect(url_for('ui.index'))

    return render_template('create_player.html', teams=teams)


@bp.route('/create_team', methods=['GET', 'POST'])
#@login_required
def create_team():
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))
    
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Team(name=name))
        db.session.commit()
        flash('Team added successfully!')
        return redirect(url_for('ui.index'))
    return render_template('create_team.html')

@bp.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
@bp.input(LoginIn, location='form')
def login_post(form_data=None):

    email = form_data['email']
    password = form_data['password']

    # print("POST to", f'{API_BASE}/users/login')
    # print("Request Payload:", {'email': email, 'password': password})

    data = authenticate_user(email, password)
    if data:
        session['auth_token'] = data['token']
        session['user_id'] = data['user_id']
        flash('Login successful', 'success')
        return redirect(url_for('ui.index'))
    else:
        return redirect(url_for('ui.login_get'))

@bp.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@bp.route('/register', methods=['POST'])
@bp.input(UserIn, location='form')
def register_post(form_data=None):

    name = form_data['name']
    email = form_data['email']
    password = form_data['password']
    
    user = User(**form_data)
    db.session.add(user)
    db.session.commit()

    flash('Registrierung erfolgreich! Bitte einloggen.', 'success')
    return redirect(url_for('ui.login_get'))

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('ui.index'))

@bp.route("/teams/<int:team_id>")
def view_team(team_id):
    team = Team.query.get_or_404(team_id)
    return render_template("team_detail.html", team=team)

@bp.route("/players/<int:player_id>/change_team", methods=["POST"])
def change_team(player_id):
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))

    player = Player.query.get_or_404(player_id)
    team_id = request.form.get("team_id")

    if team_id:
        team = Team.query.get(team_id)
        player.team = team
    else:
        player.team = None

    db.session.commit()
    return redirect(url_for('ui.view_player', player_id=player.id))


@bp.route("/players/<int:player_id>")
def view_player(player_id):
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))

    player = Player.query.get_or_404(player_id)
    teams = Team.query.all()
    return render_template("player_detail.html", player=player, teams=teams)

@bp.route("/tournaments/<int:tournament_id>/teams", methods=["GET", "POST"])
def manage_tournament_teams(tournament_id):
    token = session.get('auth_token')
    user_id = session.get('user_id')

    if not token:
        flash("Bitte einloggen", "warning")
        return redirect(url_for('ui.login_get'))

    tournament = Tournament.query.get_or_404(tournament_id)
    all_teams = Team.query.all()
    current_team_ids = {tt.team_id for tt in tournament.teams}

    if request.method == "POST":
        selected_team_id = int(request.form["team_id"])
        if selected_team_id not in current_team_ids:
            new_assignment = TournamentTeam(tournament_id=tournament.id, team_id=selected_team_id)
            db.session.add(new_assignment)
            db.session.commit()
        return redirect(url_for("ui.manage_tournament_teams", tournament_id=tournament.id))

    return render_template("manage_tournament_teams.html", tournament=tournament, all_teams=all_teams, tournament_id=tournament_id)