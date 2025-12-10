from flask_sqlalchemy import SQLAlchemy
from app.models.user import User
from app.models.team import Team
from marshmallow import Schema, fields

from app.extensions import db

class PlayerOut(Schema):
    id = fields.Int()
    summoner_name = fields.Str()
    tag = fields.Str()
    puuid = fields.Str()
    team_id = fields.Int()

class PlayerIn(Schema):
    summoner_name = fields.Str(required=True)   
    tag = fields.Str(required=True)
    team_id = fields.Int()

class PlayerTeamUpdateIn(Schema):
    team_id = fields.Int(required=True)

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    summoner_name = db.Column(db.String(100), unique=True, nullable=False)
    tag = db.Column(db.String(10), nullable=False)
    puuid = db.Column(db.String(100), unique=True, nullable=True)
    summoner_level = db.Column(db.Integer, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    team = db.relationship("Team", back_populates="players")
 #   team = db.relationship('Team', back_populates='players')
 #   created_by = db.relationship('User')

