from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import FriendRequest, User, Friend

friend = Blueprint('friend', __name__)

@friend.route('/add_friend', methods=['POST'])
def add_friend():
    if request.method == 'POST':
        friend_name = request.form['friend_name']

        ami_exist = User.query.filter_by(login=friend_name).first()

        if ami_exist:
            existing_request = FriendRequest.query.filter_by(sender_id=1, receiver_id=ami_exist.id, accepted=False).first()

            if existing_request:
                flash(f"Une demande d'ami est déjà en attente pour {friend_name}.", category='error')
            else:
                current_user = User.query.filter_by(login='utilisateur_actuel').first()
                new_request = FriendRequest(sender_id=current_user.id, receiver_id=ami_exist.id)
                db.session.add(new_request)
                db.session.commit()
                flash(f"Demande d'ami envoyée à {friend_name}. Attendez la confirmation.", category='success')

        else:
            flash(f"{friend_name} n'existe pas.", category='error')

    return redirect(url_for('views.home'))

@friend.route('/friend_demand')
def friend_demand():
    current_user = User.query.filter_by(login='utilisateur_actuel').first()
    friend_requests = FriendRequest.query.filter_by(receiver_id=current_user.id, accepted=False).all()
    return render_template('demandes_amis.html', friend_requests=friend_requests)

@friend.route('/accept_demand/<int:demande_id>')
def accept_demand(demande_id):
    friend_request = FriendRequest.query.get(demande_id)

    if friend_request:
        friend_request.accepted = True

        friend_entry_1 = Friend(user_id=friend_request.sender_id, friend_id=friend_request.receiver_id)
        friend_entry_2 = Friend(user_id=friend_request.receiver_id, friend_id=friend_request.sender_id, reciprocal=True)

        db.session.add_all([friend_entry_1, friend_entry_2])
        db.session.commit()

        flash(f"Vous êtes maintenant ami avec {friend_request.sender.name}.", category='success')
    else:
        flash("Demande d'ami introuvable.", category='error')

    return redirect(url_for('friend.friend_demand'))
