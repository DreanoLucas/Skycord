from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
  return render_template('page_accueil.html', user=current_user)
