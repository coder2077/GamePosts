from flask_login import UserMixin
from . import login_manager
from . import db


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)


# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50), nullable=False, unique=False)
    image = db.Column(db.LargeBinary(), nullable=False, unique=False)
    author = db.Column(db.String(length=60), nullable=False, unique=False)
    description = db.Column(db.String(length=3000), nullable=False, unique=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
