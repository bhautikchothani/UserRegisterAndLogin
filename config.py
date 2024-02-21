import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

#mysql://username:password@hostname:port/database_name

SQLALCHEMY_DATABASE_URI = "mysql://bhautik:bhautikpassword@0.0.0.0:5506/skillupserve"

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY="bhautik"

SESSION_PERMANENT = False

SESSION_TYPE = "filesystem" # default is 'memory', can be changed to any session type accepted by Flask