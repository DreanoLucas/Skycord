"""Handles the database models for user authentication and message storage.

This script defines two SQLAlchemy models: 'User' and 'Message'. 
- 'User' represents user details and authentication information.
- 'Message' stores messages associated with users.

Classes:
    Message: Represents stored messages, linked to User.
    User: Represents user details and authentication.

Dependencies:
    - db: The database instance.
    - UserMixin: Flask-Login helper class for User model.

Note:
    Ensure the models align with your application's authentication and message storage requirements.
"""


from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(50), unique=True, nullable=False)
  login = db.Column(db.String(30), unique=True, nullable=False)
  password = db.Column(db.String(20), nullable=False)
  name = db.Column(db.String(20), nullable=False)
  profil = db.Column(db.String(250)) 
  message = db.relationship('Message')  # pas compris l'utilité
  confirmed = db.Column(db.Boolean, default=False)
  token = db.Column(db.String(100))
  friends = db.relationship('Friend', foreign_keys='Friend.user_id', backref='user', lazy=True)


class Chat(db.Model):
  chat_id = db.Column(db.Integer, primary_key=True)
  chat_name = db.Column(db.String(100))
  is_group = db.Column(db.Boolean, default=False) # a voir si c'est utile


class ChatMember(db.Model):
  chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  text = db.Column(db.String(1000), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'))

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reciprocal = db.Column(db.Boolean, default=False)
    
class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accepted = db.Column(db.Boolean, default=False)
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
