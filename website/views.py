"""Defines routes and views for the application.

This script contains routes and views using Flask's Blueprint functionality.
It includes a route for the home page ('/') that renders the 'acceuil.html' template.

Blueprints:
    views: Blueprint for handling application views and routes.

Functions:
    home: Renders the home page, ensuring the user is logged in using Flask-Login's login_required.

Dependencies:
    - Flask: Micro web framework for Python.
    - Blueprint: Flask feature for organizing routes.
    - render_template: Function to render HTML templates.
    - login_required: Decorator from Flask-Login for requiring login to access routes.
    - current_user: Function from Flask-Login to get the current logged-in user.
"""

from flask import Blueprint, render_template, url_for, redirect, session
from flask_login import login_required, current_user
from . import db
from .models import *
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():

    """Renders the home page.

    Checks if the user is logged in (using Flask-Login's login_required decorator).
    If logged in, renders the 'acceuil.html' template, passing the current user's information.

    Returns:
        Rendered template: Renders the 'acceuil.html' template with user information.
    """

    
    subquery = db.session.query(Message.chat_id,
                              func.max(
                                  Message.date).label('max_date')).group_by(
                                      Message.chat_id).subquery()

    user_chats = db.session.query(
      Chat.chat_id, Chat.chat_name, Message.text,
      Message.date).join(ChatMember, ChatMember.chat_id == Chat.chat_id).join(
            User, User.id == ChatMember.user_id).join( subquery, subquery.c.chat_id == Chat.chat_id, isouter=True).join(
                    Message,
                    db.and_(Message.chat_id == Chat.chat_id, Message.date == subquery.c.max_date), isouter=True).filter(
                            User.id == current_user.id).order_by(Message.date.desc())

    messages = session.pop('sorted_messages', None)
    receiverName = ""
    if messages:
        receiverName = messages[0]['Receiver']
    return render_template('page_accueil.html',
                            user=current_user,
                            username = receiverName,
                            chats=user_chats.all(),
                            messages=messages)
