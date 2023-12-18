
from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from .models import User 
from . import db, mail
import secrets
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message


auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():

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
    logout_user()

    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

    if(request.method == 'POST'):
        _username = request.form.get("username")
        _email  = request.form.get("email")
        _password = request.form.get("password")

        user = User.query.filter_by(login=_username).first()

        if user:
            flash("Compte déjà existant", category='error')

        elif(len(_email) < 4): flash('Email trop courte', category='error')
        elif(len(_username) < 4): flash('Nom trop court, au moins 4 caractères est nécessaire ', category='error')
        elif(len(_password) < 7): flash('Mot de passe trop court, au moins 7 caractères est nécessaire', category='error')
        
        else : 
            new_user = User(email=_email, login=_username, name=_username, password=generate_password_hash(_password, method='pbkdf2:sha256'), token= secrets.token_urlsafe(30))

            db.session.add(new_user)
            db.session.commit()
            send_confirmation_email(new_user)
            flash('Un email de confirmation a été envoyé à votre adresse.', category='success')
            return render_template("page_de_connexion.html")
    return render_template("page_inscription.html")






def send_confirmation_email(user):

    msg = Message('Confirmation de compte', sender='skycord.code@gmail.com', recipients=[user.email])
    token = user.token
    print(token)
    msg.body = f"Pour confirmer votre compte, veuillez cliquer sur le lien suivant: {url_for('auth.confirm_account', token=token, _external=True)}"
    print(msg.body)
    mail.send(msg)
    

@auth.route('/confirm_account/<token>')
def confirm_account(token):
    user = User.query.filter_by(token=token).first()

    if user:
        user.confirmed = True
        user.token = None  
        db.session.commit()
        login_user(user, remember=True)
        flash('Votre compte a été confirmé avec succès!', category='success')
    else:
        flash('Le lien de confirmation est invalide ou a expiré.', category='error')

    return render_template("acceuil.html", user=user)
