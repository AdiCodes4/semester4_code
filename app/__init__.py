from apiflask import APIFlask
from flask import Flask, redirect, url_for, session, render_template, flash
from config import Config
from app.extensions import db
from flask_migrate import Migrate
from flask_cors import CORS

def create_app(config_class=Config):
    app = APIFlask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # Flask Erweiterungen initialisieren
    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprints registrieren
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.teams import bp as teams_bp
    app.register_blueprint(teams_bp, url_prefix='/teams')

    from app.players import bp as players_bp
    app.register_blueprint(players_bp, url_prefix='/players')

    from app.tournament import bp as tournament_bp
    app.register_blueprint(tournament_bp, url_prefix='/tournament')

    from app.ui import bp as ui_bp
    app.register_blueprint(ui_bp, url_prefix='/ui')

    with app.app_context():
        #db.drop_all()  # Nur für Entwicklungszwecke, in Produktion nicht verwenden
        db.create_all()

    @app.route('/')
    def default():
        return redirect(url_for('ui.login_get'))
    
#    def index():
#        tournaments = Tournament.query.all()
#        return render_template('index.html', tournaments=tournaments)
#    def test_page():
#        return {'message': 'Blueprint Flask - Production Setup (Turnierbaum Generator) - v1.0'}

    return app
