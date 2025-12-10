from apiflask import APIBlueprint

bp = APIBlueprint('tournament', __name__)

from app.tournament import routes
