
from app.extensions import db
from app.models.team import Team
from app.models.player import Player
from app.models.matchup import Matchup
from app.models.tournament import Tournament
from app.models.user import User

# Hilfsfunktion (Testdaten erstellen, Tabellen erstellen)
def create_test_data():
    db.drop_all() # dieser Befehl löscht alle vorhandenen Datenbankeintraege und Tabellen
    db.create_all()

    # Beispieldaten
    users = [
        {'name': 'testuser1', 'email': 'testuser1@testmail.ch', 'password': 'Test%1234'},
        {'name': 'testuser2', 'email': 'testuser2@testmail.ch', 'password': 'Test%1234'},
        {'name': 'testuser3', 'email': 'testuser3@testmail.ch', 'password': 'Test%1234'},
        {'name': 'testuser4', 'email': 'testuser4@testmail.ch', 'password': 'Test%1234'}
    ]
    for user_data in users:
        user = User(**user_data)
        db.session.add(user)

    teams = [
        {'name': 'Team1'},
        {'name': 'Team2'},
        {'name': 'Team3'},
        {'name': 'Team4'},
    ]
    for team_data in teams:
        team = Team(**team_data)
        db.session.add(team)

    players = [
        {'summoner_name': 'müesli', 'tag': 'EUW', 'team_id': '1'},
        {'summoner_name': 'YomSmasher', 'tag': 'EUW', 'team_id': '2'},
        {'summoner_name': 'kalast', 'tag': 'EUW', 'team_id': '3'},
        {'summoner_name': 'Atli', 'tag': '2653', 'team_id': '4'}
    ]
    for player_data in players:
        player = Player(**player_data)
        db.session.add(player)

    # create a tournament
    tournament = Tournament(name='Test Tournament')
    db.session.add(tournament)


    db.session.commit()