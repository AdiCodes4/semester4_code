from flask_sqlalchemy import SQLAlchemy
from app.models.user import User
from app.models.team import Team
from marshmallow import Schema, fields

from app.extensions import db

class MatchupOut(Schema):
    id = fields.Int()
    summoner_name = fields.Str()
    team_id = fields.Int()

class MatchupIn(Schema):
    summoner_name = fields.Str(required=True)
    team_id = fields.Int()

class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    team1_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team2_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)

    team1 = db.relationship('Team', foreign_keys=[team1_id])
    team2 = db.relationship('Team', foreign_keys=[team2_id])