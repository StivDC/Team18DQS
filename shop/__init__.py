from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '9e46baba727119686172c5d5ec8c94f31312a51baf966d6d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://group28.2018:jncPzvP4TVNF6gt@csmysql.cs.cf.ac.uk:3306/group28.2018'
app.jinja_env.filters['zip'] = zip

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
