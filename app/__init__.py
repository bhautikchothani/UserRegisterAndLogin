from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_mail import Mail
from flask_migrate import Migrate


app  = Flask(__name__)

app.config['MAIL_USERNAME'] = 'hautikchothani51@gmail.com' ##this mail use to send company mail##
app.config['MAIL_PASSWORD'] = 'iplpxgiqfekvsnpa'  # Your email 2 step verfication password generate use it ###

bcrypt =Bcrypt(app)

app.config.from_object('config')
Session(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
mail = Mail(app)
from app import routes, models

