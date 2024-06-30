from flask import Flask
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()


# Create Flask-App
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.config['SQLALCHEMY_DATABASE_URI'] = DevelopmentConfig.SQL_DATABASE_URI
    db.init_app(app)

    # import Blueprints
    from .views import views
    from .auth import auth

   # Register Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    from .models import User

    with app.app_context():
        db.create_all()

    return app
 