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


""" 
Avec les tables actuel pour recuperer les chats de l'utilisateur. 

SELECT C.chat_id, c.chat_name, M.text
FROM user U
JOIN chat_member CM ON CM.user_id = U.id
JOIN chat C ON C.chat_id = CM.chat_id

JOIN (
    SELECT chat_id, MAX(date) AS max_date
    FROM Message
    GROUP BY chat_id
) MAX ON C.chat_id = MAX.chat_id

JOIN message M ON 
M.chat_id = C.chat_id 
AND M.date = MAX.max_date
WHERE U.id = -- Mettre l'id de l'utilisateur ici
ORDER By M.date DESC



INSERT INto chat VALUES (1, 'test', 0)
INSERT INTO chat_member VALUES (1, 4)
INSERT INTO chat_member VALUES (1, 3)

INSERT INTO Message (date, text, user_id, chat_id)
VALUES (datetime('now'), 'test', 3, 1);
"""