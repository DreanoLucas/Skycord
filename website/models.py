from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True, nullable=False)
  login = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  name = db.Column(db.String(100), nullable=False)
  message = db.relationship('Message')  # pas compris l'utilité
  confirmed = db.Column(db.Boolean, default=False)
  token = db.Column(db.String(100))


class Chat(db.Model):
  chat_id = db.Column(db.Integer, primary_key=True)
  chat_name = db.Column(db.String(50), unique=True, nullable=False)
  is_group = db.Column(db.Boolean, default=False)


class ChatMember(db.Model):
  chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'), primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  text = db.Column(db.String(1000), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'))


""" 
/!\ A tester : 

Avec les tables actuel pour recuperer les groupes de l'utilisateur. 
select C.*, U2.name from user U

join ChatMember CM on 
	U.id = CM.user_id

join Chat C ON
	CM.chat_id = CM.chat

join Message M ON
	M.date = max(M.Date) 
	C.chat_id = M.chat_id 

join user U2
	M.user_id = U2.user_id

Order by M.date DESC
"""
