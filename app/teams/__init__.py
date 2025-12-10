from apiflask import APIBlueprint

bp = APIBlueprint('teams', __name__)

from app.teams import routes
