from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from app.extensions import db

class TournamentOut(Schema):
    id = fields.Int()
    name = fields.Str()
    teams = fields.Nested("TournamentTeamOut", many=True)

class TournamentIn(Schema):
    name = fields.Str(required=True)

class TournamentTeamOut(Schema):
    id = fields.Int()
    team_id = fields.Int()
    tournament_id = fields.Int()

class TournamentTeamIn(Schema):
    team_id = fields.Int(required=True)
    tournament_id = fields.Int(required=True)


class Tournament(db.Model):
    __tablename__ = 'tournaments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    teams = db.relationship('TournamentTeam', back_populates='tournament', cascade='all, delete-orphan')


class TournamentTeam(db.Model):
    __tablename__ = 'tournament_teams'

    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

    tournament = db.relationship('Tournament', back_populates='teams')
    team = db.relationship('Team', back_populates='tournament_assignments')
