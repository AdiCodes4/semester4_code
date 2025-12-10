from apiflask import APIBlueprint

bp = APIBlueprint('players', __name__)

from app.players import routes
