from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '9e46baba727119686172c5d5ec8c94f31312a51baf966d6d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1846366:Monopoly@csmysql.cs.cf.ac.uk:3306/c1846366'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
