from app.teams import bp
from flask import request, jsonify
from app.models.team import Team, db
from app.models.team import TeamIn, TeamOut
from auth.auth import token_auth
from app.models.player import Player
from app.models.tournament import Tournament, TournamentOut

# get all teams
@bp.get('/')
@bp.auth_required(token_auth)
@bp.output(TeamOut(many=True))
def get_all_Teams():
    teams = Team.query.all()
    return teams

# get team by name
@bp.get('/<string:team_name>')
@bp.auth_required(token_auth)
@bp.output(TeamOut)
def get_team_by_name(team_name):
    team = Team.query.filter_by(name=team_name).first()
    if not team:
        return jsonify({'message': 'Team not found'}), 404
    return TeamOut.dump(team), 200

# get team by id
@bp.get('/<int:team_id>')
@bp.auth_required(token_auth)
@bp.output(TeamOut)
def get_team(team_id):
    return db.get_or_404(Team, team_id)

# create team
@bp.post('/')
@bp.auth_required(token_auth)
@bp.input(TeamIn, location='json')
@bp.output(TeamIn, status_code=201)
def create_team(json_data):
    team = Team(**json_data)
    db.session.add(team)
    db.session.commit()
    return team, 201

# update team
@bp.put('/<int:team_id>/name')
@bp.auth_required(token_auth)
@bp.input(TeamIn(partial=('players',)), location='json')  # Accept only 'name'
@bp.output(TeamOut, status_code=200)
def update_team_name(team_id, json_data):
    team = Team.query.get_or_404(team_id)

    if 'name' in json_data:
        team.name = json_data['name']
        db.session.commit()

    return team

# delete team
@bp.delete('/<int:team_id>')
@bp.auth_required(token_auth)
@bp.output({}, status_code=204)
def delete_team(team_id):
    team = db.get_or_404(Team, team_id)
    db.session.delete(team)
    db.session.commit()
    return ''    