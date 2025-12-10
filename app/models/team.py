from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate

from app.extensions import db

class TeamOut(Schema):
    id = fields.Int()
    name = fields.Str()
    players = fields.Nested("PlayerOut", many=True)

class TeamIn(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

 #   players = db.relationship('Player', back_populates='team', cascade='all, delete-orphan')
    players = db.relationship("Player", foreign_keys='Player.team_id', cascade='all, delete-orphan')
    tournament_assignments = db.relationship('TournamentTeam', back_populates='team', cascade='all, delete-orphan')


