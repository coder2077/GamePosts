from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



# init SQLAlchemy so we can use it later in our models
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dpuiqcxkehbndo:51e10441db80201464b871b3f4a1374354eac5bbc8db4775d5929220bcd9a6ef@ec2-18-207-72-235.compute-1.amazonaws.com:5432/dcea9gebgng3mu'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
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

