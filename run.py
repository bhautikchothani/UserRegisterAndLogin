from app import app ,db
from app.models import Credentials

if __name__ == '__main__':
    # print("Starting the flask app with app.run")
    # app.run(debug=True)
    # print("Creating table !!")
    # db.create_all()
    # print(f"Database tables created , {db.create_all()}")
    with app.app_context():
        db.create_all()   
        print("Starting the flask app with app.run")
        app.run(debug=True)