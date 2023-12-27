#faudrait deplacer le sql dans un fichier sqlrequest.py mais deja je voudrais savoir si ça marche

from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

from . import db
from .models import *

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
  subquery = db.session.query(Message.chat_id,
                              func.max(
                                  Message.date).label('max_date')).group_by(
                                      Message.chat_id).subquery()

  user_chats = db.session.query(
      Chat.chat_id, Chat.chat_name, Message.text,
      Message.date).join(ChatMember, ChatMember.chat_id == Chat.chat_id).join(
          User, User.id == ChatMember.user_id).join(
              subquery, subquery.c.chat_id == Chat.chat_id).join(
                  Message,
                  db.and_(Message.chat_id == Chat.chat_id,
                          Message.date == subquery.c.max_date)).filter(
                              User.id == current_user.id).order_by(
                                  Message.date.desc())

  print(user_chats.all())
  return render_template('page_accueil.html',
                         user=current_user,
                         chats=user_chats.all())
