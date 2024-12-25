from . import db
from flask_login import UserMixin
from datetime import datetime

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(162), nullable = False)
    is_admin = db.Column(db.Boolean, default=False)
    initiatives = db.relationship('initiative', backref='user', lazy=True)


class articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable = False)
    article_text = db.Column(db.Text, nullable = False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer)


class initiative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    is_public = db.Column(db.Boolean)
    votes = db.Column(db.Integer, default=0) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
