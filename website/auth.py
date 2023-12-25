from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User 
from . import db

from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if(request.method == 'POST'):
        _username = request.form.get("username")
        _password = request.form.get("password")

        user = User.query.filter_by(login=_username).first()
        if user:
            if check_password_hash(user.password, _password):
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
        email = User.query.filter_by(email=_email).first()
        if user:
            flash("Compte déjà existant", category='error')
        elif email : flash(f"email déjà attribuée au compte {email.login}", category='error')
        elif(len(_email) < 4): flash('Email trop courte', category='error')
        elif(len(_username) < 4): flash('Nom trop court, au moins 4 caractères est nécessaire ', category='error')
        elif(len(_password) < 7): flash('Mot de passe trop court, au moins 7 caractères est nécessaire', category='error')
        
        else : 
            new_user = User(email=_email, login=_username, name=_username, password=generate_password_hash(_password, method='pbkdf2:sha256'))

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Compte créé', category='success')
            return redirect(url_for('views.home'))

    return render_template("page_inscription.html")