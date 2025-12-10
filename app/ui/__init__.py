from apiflask import APIBlueprint

bp = APIBlueprint('ui', __name__)

from app.ui import routes