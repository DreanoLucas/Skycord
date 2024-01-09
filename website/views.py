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

from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user
from . import db
from .models import *
views = Blueprint('views', __name__)

from sqlalchemy import func, case
from sqlalchemy.orm import aliased

@views.route('/')
@login_required
def home():
    """Renders the home page.

    Checks if the user is logged in (using Flask-Login's login_required decorator).
    If logged in, renders the 'acceuil.html' template, passing the current user's information.

    Returns:
        Rendered template: Renders the 'acceuil.html' template with user information.
    """
    from sqlalchemy import text, create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    user_id = current_user.id
    query = text("""
        SELECT chat.chat_id AS chat_chat_id, chat.chat_name AS chat_chat_name, message.text AS message_text, message.date AS message_date 
        FROM chat
        JOIN chat_member ON chat_member.chat_id = chat.chat_id
        JOIN user ON user.id = chat_member.user_id
        LEFT OUTER JOIN (
            SELECT message.chat_id AS chat_id, max(message.date) AS max_date
            FROM message GROUP BY message.chat_id
        ) AS anon_1 ON anon_1.chat_id = chat.chat_id
        LEFT OUTER JOIN message ON message.chat_id = chat.chat_id AND message.date = anon_1.max_date
        WHERE user.id = :user_id
        ORDER BY CASE WHEN message_date IS NULL THEN 0 ELSE 1 END, message_date DESC;
    """)


    user_chats = session.execute(query, {"user_id": user_id})
    session.close()
    return render_template('page_accueil.html',
                            user=current_user,
                            chats=user_chats.all()
                            )
