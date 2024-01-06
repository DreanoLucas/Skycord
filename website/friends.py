"""
Manages friend-related routes and functionalities for the Flask application.

This script contains routes and functions for friend-related functionalities within the Flask application.
It includes routes for adding friends, handling friend requests, displaying friend lists, and managing friend groups.
Additionally, it interacts with the database models for users and friend-related operations.

Blueprints:
    friend: Blueprint for handling friend-related routes.

Functions:
    ajouter: Displays a list of pending friend requests for the current user.
    friend_demand: Displays pending friend requests for the current user.
    groupe: Renders the group page for friends.
    parametre: Renders the settings page for friend-related settings.
    add_friend: Handles the addition of a new friend by sending a friend request.
    accept_demand: Handles the acceptance of a friend request.

Dependencies:
    - Blueprint: Flask feature for organizing routes.
    - render_template: Function to render HTML templates.
    - request: Object to handle HTTP requests.
    - flash: Function to display flashed messages.
    - redirect: Function to redirect to different routes.
    - url_for: Function to generate URLs for routes.
    - Flask-Login: Flask extension for managing user sessions.
    - db: The database instance.
    - FriendRequest, User, Friend: Models for friend-related operations from the .models module.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from flask_login import current_user, login_required

from .models import FriendRequest, User, Friend

friend = Blueprint('friend', __name__)

@friend.route('/ajouter')
@login_required
def ajouter():
    """
    Displays a list of pending friend requests for the current user.

    Returns:
        template: Renders the 'ajouter.html' page with data of pending friend requests.
    """
    amisDemandeListe = []

    friend_requests = FriendRequest.query.filter_by(receiver_id=current_user.id, accepted=False).all()
    for i in friend_requests:
        amisDemandeListe.append(User.query.filter_by(id=i.sender_id).first())
    return render_template('ajouter.html', donnees=amisDemandeListe)

@friend.route('/friend_demand')
@login_required
def friend_demand():
    """
    Displays pending friend requests for the current user.

    Returns:
        template: Renders the 'ajouter.html' page with pending friend requests.
    """
    current_user = User.query.filter_by(login='current_user').first()
    friend_requests = FriendRequest.query.filter_by(receiver_id=current_user.id, accepted=False).all()
    return render_template('ajouter.html', friend_requests=friend_requests)

@friend.route('/groupe')
@login_required
def groupe():
    """
    Renders the group page for friends.

    Returns:
        template: Renders the 'groupe.html' page.
    """
    return render_template('groupe.html')

@friend.route('/parametre')
@login_required
def parametre():
    """
    Renders the settings page for friend-related settings.

    Returns:
        template: Renders the 'page_parametre.html' page.
    """
    return render_template('page_parametre.html')

@friend.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    """
    Handles adding a new friend by sending a friend request.

    Returns:
        redirection: Redirects to the home page ('views.home') after processing the request.
    """
    if request.method == 'POST':
        friend_name = request.form['friend_name']

        ami_exist = User.query.filter_by(login=friend_name).first()
        if ami_exist:
            existing_request = FriendRequest.query.filter_by(sender_id=1, receiver_id=ami_exist.id, accepted=False).first()

            if existing_request:
                flash(f"A friend request is already pending for {friend_name}.", category='error')
            else:
                current_user = User.query.filter_by(login='current_user').first()
                new_request = FriendRequest(sender_id=current_user.id, receiver_id=ami_exist.id)
                db.session.add(new_request)
                db.session.commit()
                flash(f"Friend request sent to {friend_name}. Please wait for confirmation.", category='success')

        else:
            flash(f"{friend_name} does not exist.", category='error')

    return redirect(url_for('views.home'))

@friend.route('/accept_demand/<int:demande_id>', methods=['POST'])
def accept_demand(demande_id):
    """
    Handles the acceptance of a friend request.

    Args:
        demande_id (int): The ID of the friend request to accept.

    Returns:
        redirection: Redirects to the friend_demand route after processing the request.
    """
    friend_request = FriendRequest.query.get(demande_id)

    if friend_request:
        friend_request.accepted = True

        friend_entry_1 = Friend(user_id=friend_request.sender_id, friend_id=friend_request.receiver_id)
        friend_entry_2 = Friend(user_id=friend_request.receiver_id, friend_id=friend_request.sender_id, reciprocal=True)

        db.session.add_all([friend_entry_1, friend_entry_2])
        db.session.commit()

        flash(f"You are now friends with {friend_request.sender.name}.", category='success')
    else:
        flash("Friend request not found.", category='error')

    return redirect(url_for('friend.friend_demand'))
