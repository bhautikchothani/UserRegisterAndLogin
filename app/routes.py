from flask import request, redirect, render_template, flash,session,current_app,url_for
from app import app, db
from app.models import Credentials,ContactUs
from flask import after_this_request
from flask_sqlalchemy import SQLAlchemy
import secrets
import os   
from werkzeug.utils import secure_filename
from flask_mail import Mail,Message,_MailMixin

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg',}
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
app.config["UPLOAD_FOLDER"] = "app/static/images"

## mail##
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True 
app.config['MAIL_USERNAME'] = 'bhautikchothani51@gmail.com' ##this mail use to send company mail##
app.config['MAIL_PASSWORD'] = 'iplpxgiqfekvsnpd'  # Your email 2 step verfication password generate use it ###
mail = Mail(app)

# Function to check if a filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET','POST'])
def homepage():
    return render_template('home.html')




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        username = request.form['username'] 
        password = request.form['password']
        phone_number = request.form['phone_number']
        photo = request.files['photo']
        
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = "default.jpg"

        new_user = Credentials(username=username,phone_number=phone_number,photo=filename)
        new_user.set_password(password)
        db.session.add(new_user)  # Add the new user to the database session ##
        db.session.commit()  ## save the data ##
        return redirect('/login')
        
    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login_data():

    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]
        user = Credentials.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                 # Store username in session
                session['id'] = user.id
                session['username'] = user.username
                session['phone_number'] = user.phone_number
                session['photo'] = user.photo
                flash("login successfully !!")
                return render_template("index.html",username=username)
            else:
                error_message = "Invalid Password"
        else:
            error_message = "invalid username"
        flash(error_message)
    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
        if 'username' in session:  # Check if the user is logged in
            user_profile = {
                'id': session.get('id'),
                'username': session.get('username'),
                'phone_number': session.get('phone_number'),
                'photo': session.get('photo')  # Assuming 'photo' contains the filename
            }
            return render_template('Profile.html', user_profile=user_profile)
    return redirect('/')


def add_header(response):
    response.headers["Cache-Control"] = ("no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0")
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1" 
    return response

@app.route('/logout', methods=['GET','POST'])
def  logout():
    session.pop('username',None)
    session.pop('phone_number',None)
    session.clear()

    @after_this_request
    def add_no_cache_header(response):
        response.headers["Cache-Control"] = ("no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0")
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response
    return render_template('home.html')

@app.route("/edit/<int:id>", methods=['GET','POST'])
def edit(id):
    user = Credentials.query.filter_by(id=id).first()
    return render_template("update.html",user=user)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = Credentials.query.get(id)

    if request.method == "POST" and user:
        username = request.form.get("username")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        photo = request.form.get("photo")

        # Check if 'photo' is present in request.files
        if 'photo' in request.files:
            photo = request.files['photo']
            # Check if a new photo has been uploaded
            if photo.filename != '':
                # Delete old photo if it exists
                if user.photo:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], user.photo))
                # Save new photo
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.photo = filename

        user.update_profile(username, email, mobile,filename)
        return render_template("Profile.html", user_profile=user)
    return render_template("login.html", user_profile=user)


@app.route('/contact', methods=['POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        # Create a new instance of ContactUs model with the form data
        new_contact = ContactUs(name=name, email=email, phone=phone, message=message)

        # Add the new contact to the database session and commit changes
        db.session.add(new_contact)
        db.session.commit()
        
    
        # Send email to company
        mail.send_message("New Message From " + name,
        sender=email,
        recipients=['bhautikchothani52@gmail.com'],  # Company email address
        body=f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}')
        return render_template('home.html')
