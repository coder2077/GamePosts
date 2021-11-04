from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


UPLOAD_FOLDER = 'game/static/'

# init SQLAlchemy so we can use it later in our models
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vfyexxsiwwkfbr:7d1ec3ccbab9f022c9fc76da6c89206f2e0e43b2abff1389c35bf827b2c9889a@ec2-52-201-168-60.compute-1.amazonaws.com:5432/ddepfiifi1k3oc'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.app_context()
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

