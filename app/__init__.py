from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
app  = Flask(__name__)
from flask_migrate import Migrate

bcrypt =Bcrypt(app)

app.config.from_object('config')
Session(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
from app import routes, models
