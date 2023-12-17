from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2fa732685307e94347cb2284f1eb8e07'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Message

    with app.app_context():
        create_database()

    login_manager = LoginManager() 
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app


def create_database():
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print("Base de données créée!")