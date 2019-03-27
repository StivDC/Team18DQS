from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e91a76009f3ca7d8becd54af1c05c2f10a2bca0dd7f932e2'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1822356:Pain.Mind12345@csmysql.cs.cf.ac.uk:3306/c1822356'

#SPECIFY YOUR MYSQL CREDENTIALS:
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:MYSQL_PASSWORD@csmysql.cs.cf.ac.uk:3306/USERNAME'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
