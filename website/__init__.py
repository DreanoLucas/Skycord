"""Configures the Flask application, sets up extensions, defines routes, and initializes the database.

This file sets up the Flask application and its configurations, initializes various extensions
such as SQLAlchemy, Flask-Mail, and Flask-Login. It also defines routes using blueprints for
different parts of the application. Additionally, it includes database initialization logic.

Functions:
    create_app: Initializes and configures the Flask application.
    create_database: Creates the database if it doesn't exist within the 'website' directory.

Dependencies:
    - Flask: Micro web framework for Python.
    - Flask_SQLAlchemy: Flask extension for interacting with SQLAlchemy.
    - Flask-Mail: Flask extension for email functionality.
    - Flask-Login: Flask extension for user session management.

"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mail import Mail, Message
from flask_login import LoginManager
from . import recup_info as rc
db = SQLAlchemy()
DB_NAME = "database.db"
mail = Mail()


def create_app():
    """Creates and configures the Flask application.

    Returns:
        Flask app: The configured Flask application instance.
    """
    app = Flask(__name__)
    code_secret = rc.donnees()
    mail = Mail(app)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'skycord.code@gmail.com'
    app.config['MAIL_PASSWORD'] = code_secret['cle']
    mail.init_app(app)
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
    """Creates the database if it doesn't exist.

    Checks if the database file exists within the 'website' directory.
    """

    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print("Base de données créée!")
