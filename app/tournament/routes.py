from app.tournament import bp
from flask import Blueprint, request, jsonify
from auth.auth import token_auth
from app.models.tournament import Tournament, TournamentTeam, db
from app.models.tournament import (
    TournamentIn, TournamentOut,
    TournamentTeamIn, TournamentTeamOut
)

tournament_in_schema = TournamentIn()
tournament_out_schema = TournamentOut()
tournaments_out_schema = TournamentOut(many=True)
tournament_team_in_schema = TournamentTeamIn()
tournament_team_out_schema = TournamentTeamOut()
tournament_teams_out_schema = TournamentTeamOut(many=True)

# get all tournaments
@bp.get('/')
@bp.auth_required(token_auth)
@bp.output(TournamentOut(many=True))
def get_all_tournaments():
    tournaments = Tournament.query.all()
    return tournaments

# get tournament by id
@bp.get('/<int:tournament_id>')
@bp.auth_required(token_auth)
@bp.output(TournamentOut)
def get_tournament(tournament_id):
    return db.get_or_404(Tournament, tournament_id)

# get tournament by name
@bp.get('/<string:tournament_name>')
@bp.auth_required(token_auth)
@bp.output(TournamentOut)
def get_tournament_by_name(tournament_name):
    tournament = Tournament.query.filter_by(name=tournament_name).first()
    if not tournament:
        return jsonify({'message': 'Tournament not found'}), 404
    return TournamentOut.dump(tournament), 200

# create tournament
@bp.post('/')
@bp.auth_required(token_auth)
@bp.input(TournamentIn, location='json')
@bp.output(TournamentOut, status_code=201)
def create_tournament(json_data):
    tournament = Tournament(**json_data)
    db.session.add(tournament)
    db.session.commit()
    return tournament

# update tournament
@bp.put('/<int:tournament_id>/name')
@bp.auth_required(token_auth)
@bp.input(TournamentIn(partial=('teams', 'matches')), location='json')  # allow partial input, exclude unrelated fields
@bp.output(TournamentOut, status_code=200)
def update_tournament_name(tournament_id, json_data):
    tournament = Tournament.query.get_or_404(tournament_id)

    if 'name' in json_data:
        tournament.name = json_data['name']
        db.session.commit()

    return tournament


# delete tournament
@bp.delete('/<int:tournament_id>')
@bp.auth_required(token_auth)
@bp.output({}, status_code=204)
def delete_tournament(tournament_id):
    tournament = db.get_or_404(Tournament, tournament_id)
    db.session.delete(tournament)
    db.session.commit()
    return ''

# assign team to tournament
@bp.post('/<int:tournamet_id>/teams')
@bp.auth_required(token_auth)
@bp.input(TournamentTeamIn, location='json')
@bp.output(TournamentTeamOut, status_code=201)
def assign_team(json_data):
    assignment = TournamentTeam(**json_data)
    db.session.add(assignment)
    db.session.commit()
    return assignment, 201

# get teams in tournament
@bp.get('/<int:tournament_id>/teams>')
@bp.auth_required(token_auth)
@bp.output(TournamentTeamOut(many=True))
def get_teams_in_tournament(tournament_id):
    assignments = TournamentTeam.query.filter_by(tournament_id=tournament_id).all()
    return assignments