from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import app_config


db = SQLAlchemy()


from flask_login import LoginManager


login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "Vous devez vous connecter pour accéder à cette page."
    login_manager.login_view = "auth.login"


    migrate = Migrate(app, db)


    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Accès interdit'),403
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title="Page Non Trouvé"),404
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title="erreur serveur"),500
    @app.route('/500')
    def error():
        abort(500)

    return app