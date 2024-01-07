"""Manages user authentication-related routes and functionalities for the Flask application.

This script contains routes and functions for user authentication purposes within the Flask application.
It includes routes for user login, logout, registration, confirmation email sending, and account confirmation.
Additionally, it defines the authentication blueprint ('auth') and interacts with the database models.

Blueprints:
    auth: Blueprint for handling user authentication-related routes.

Functions:
    login: Handles user login, checking credentials and user confirmation status.
    logout: Handles user logout, terminating the current user session.
    sign_up: Handles user registration, checking input validity and creating new user accounts.
    send_confirmation_email: Sends a confirmation email for account verification.
    confirm_account: Handles user account confirmation using the provided token.

Dependencies:
    - Blueprint: Flask feature for organizing routes.
    - render_template: Function to render HTML templates.
    - request: Object to handle HTTP requests.
    - flash: Function to display flashed messages.
    - redirect: Function to redirect to different routes.
    - url_for: Function to generate URLs for routes.
    - Flask-Mail: Flask extension for email functionality.
    - User: Model for user-related operations from the .models module.
    - db: The database instance.
    - login_user, logout_user, current_user: Functions from Flask-Login for user session management.
    - generate_password_hash, check_password_hash: Functions for password hashing from werkzeug.security.
"""



from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from .models import User 
from . import db, mail
import secrets
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message


auth = Blueprint('auth', __name__)

@auth.route('/send_message/<int:receiver_id>')
def send_message(receiver_id):
    sender_id = current_user
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content='bonjour')

    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('views.home'))



@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login.

    If the request method is POST, it retrieves the username and password from the form.
    It checks if the user exists and, if confirmed, verifies the password.
    Upon successful login, it flashes a success message, logs in the user, and redirects to the home page.

    Returns:
        Flask response or rendered template: Redirects to the home page upon successful login
        or renders the login page.
    """

    if(request.method == 'POST'):
        _username = request.form.get("username")
        _password = request.form.get("password")

        user = User.query.filter_by(login=_username).first()
        if user:
            if user.confirmed == False:
                flash('e-mail non validé', category='error')
            elif check_password_hash(user.password, _password):
                flash('Connecté', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Mot de passe incorect', category='error')
        else:
            flash('Aucun compte avec ce nom existe', category='error')

 

    return render_template("page_de_connexion.html")


@auth.route('/logout')
@login_required
def logout():
    """Handles user logout.

    Logs out the current user session using Flask-Login's logout_user() function.
    Upon successful logout, it redirects the user to the login page.

    Returns:
        Flask response: Redirects to the login page after successful logout.
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """Handles user registration (sign-up).

    If the request method is POST, it retrieves the username, email, and password from the form.
    It checks if the username already exists, validates the email, username, and password length.
    If all conditions are met, it creates a new user in the database, sends a confirmation email,
    and redirects the user to the login page after successful registration.

    Returns:
        Flask response or rendered template: Redirects to the login page upon successful registration
        or renders the sign-up page with error messages.
    """

    if(request.method == 'POST'):
        _username = request.form.get("username")
        _email  = request.form.get("email")
        _password = request.form.get("password")

        user = User.query.filter_by(login=_username).first()
        email = User.query.filter_by(email=_email).first()
        if user:
            flash("Compte déjà existant", category='error')
        elif email : flash(f"email déjà attribuée au compte {email.login}", category='error')
        elif(len(_email) < 4): flash('Email trop courte', category='error')
        elif(len(_username) < 4): flash('Nom trop court, au moins 4 caractères est nécessaire ', category='error')
        elif(len(_password) < 7): flash('Mot de passe trop court, au moins 7 caractères est nécessaire', category='error')
        
        else : 
            new_user = User(email=_email, login=_username, name=_username, password=generate_password_hash(_password, method='pbkdf2:sha256'), token= secrets.token_urlsafe(30))

            db.session.add(new_user)
            db.session.commit()
            send_confirmation_email(new_user)
            flash('Un email de confirmation a été envoyé à votre adresse.', category='success')
            return redirect(url_for('auth.login'))
    return render_template("page_inscription.html")

def send_confirmation_email(user):
    """Sends a confirmation email to the user for account verification.

    Constructs and sends an email message with a confirmation link to the user's email address.
    The link contains a token for account verification, generated using the user's information.

    Args:
        user: User object: The user object containing user details (such as email and token).

    Returns:
        None
    """

    msg = Message('Confirmation de compte', sender='skycord.code@gmail.com', recipients=[user.email])
    token = user.token
    print(token)
    msg.body = f"Pour confirmer votre compte, veuillez cliquer sur le lien suivant: {url_for('auth.confirm_account', token=token, _external=True)}"
    print(msg.body)
    mail.send(msg)
    

@auth.route('/confirm_account/<token>')
def confirm_account(token):
    """Handles user account confirmation using the provided token.

    Retrieves a user based on the provided token from the URL parameters.
    If the user exists, it confirms the account by updating the 'confirmed' status and
    removing the token. It logs in the user and displays a success message.
    If the token is invalid or expired, it displays an error message.

    Args:
        token (str): The confirmation token passed in the URL.

    Returns:
        Flask response: Redirects to the home page or renders an error message.
    """
        
    user = User.query.filter_by(token=token).first()

    if user:
        user.confirmed = True
        user.token = None  
        db.session.commit()
        login_user(user, remember=True)
        flash('Votre compte a été confirmé avec succès!', category='success')
    else:
        flash('Le lien de confirmation est invalide ou a expiré.', category='error')
    return redirect(url_for('views.home'))
