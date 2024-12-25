from flask import Blueprint, redirect, render_template, request, session
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

rgz = Blueprint('rgz',__name__)

@rgz.route('/rgz/')
def lab():
    return render_template('rgz/rgz.html')
