import random
from yourapp.models import db, Team, Tournament, Matchup

def create_randomized_matchups(tournament_id):
    # Fetch teams from DB
    teams = Team.query.all()
    team_ids = [team.id for team in teams]
    
    if len(team_ids) < 2:
        raise ValueError("Not enough teams to create matchups.")

    random.shuffle(team_ids)

    # Pair up teams
    matchups = []
    while len(team_ids) >= 2:
        team1 = team_ids.pop()
        team2 = team_ids.pop()
        matchup = Matchup(
            tournament_id=tournament_id,
            team1_id=team1,
            team2_id=team2
        )
        matchups.append(matchup)

    # If an odd number of teams, one gets a bye
    if team_ids:
        team1 = team_ids.pop()
        matchup = Matchup(
            tournament_id=tournament_id,
            team1_id=team1,
            team2_id=None  # Bye
        )
        matchups.append(matchup)

    # Save to database
    db.session.add_all(matchups)
    db.session.commit()

    return matchups
