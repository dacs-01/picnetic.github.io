#------------------------------------------------------------------------------------------------------------------------------------------                            _       
 #(_)                          | |      
 # _ _ __ ___  _ __   ___  _ __| |_ ___ 
 #| | '_ ` _ \| '_ \ / _ \| '__| __/ __|
 #| | | | | | | |_) | (_) | |  | |_\__ \
 #|_|_| |_| |_| .__/ \___/|_|   \__|___/
 #           | |                       
 #           |_|     
import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, abort, url_for, session, url_for
#imports for the recaptcha
from form import captchaForm
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

from src.models import db, Users, Comments
import base64

import io

from src.repositories.users_repository import users_repository_singleton

#------------------------------------------------------------------------------------------------------------------------------------------

app = Flask(__name__)

bcrypt = Bcrypt(app)
#------------------------------------------------------------------------------------------------------------------------------------------
#                                          __ _                       _   _             
#     /\                                  / _(_)                     | | (_)            
#    /  \   _ __  _ __     ___ ___  _ __ | |_ _  __ _ _   _ _ __ __ _| |_ _  ___  _ __  
#   / /\ \ | '_ \| '_ \   / __/ _ \| '_ \|  _| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \ 
#  / ____ \| |_) | |_) | | (_| (_) | | | | | | | (_| | |_| | | | (_| | |_| | (_) | | | |
# /_/    \_\ .__/| .__/   \___\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_|
#          | |   | |                             __/ |                                  (keys and things)
#          |_|   |_|                            |___/                                   
#2 recaptcha keys. The site key and then the site secret key. 
#if you want to make your own:  got to the https://developers.google.com/recaptcha/intro and click on "sing up for an API key pair"
# from there, you create a website and make sure to click reCaptcha v2. For domains, put down the 127.0.0.1 and localhost as the domains. 
# For secuirty preference, I put it in the middle between easiest and most secure
#when you click save, it should give you your 2 keys which you will then put in the .env file. 
#it might take a few days for you to get the recaptcha information in the analytics center. 
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
APP_SECRET = os.environ.get("APP_SECRET")

#the secret key for the flask site. Makes sure sessions are protected. I generated a random key using os.urandom()
app.config['SECRET_KEY'] = APP_SECRET
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
#------------------------------------------------------------------------------------------------------------------------------------------


#This is the dotenv connection string for our database
load_dotenv()

db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '3306')
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME', 'picnetic_db')

connection_string = f'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
picFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/', methods =['GET'])
def index():

    #check if the user is in the session
    if 'user' in session:
        #FAKE INFORMATION FOR TESTING -----------------------------------------
        bio = "HI"
        photo = "static/images/sportsphoto1.jpg"
        imgType = "sports"
        #------------------------------------------
        #if the user makes a post request 
        if request.method == 'POST':
            #get the comment
            comment = request.form.get("comment", '')
            #check if the comment is real
            if comment != '':
                #PUT A POST ID HERE
                #if it is real then create the comment and add it to the DB
                #BLOEKC HERE BLOCKED HERE
                #BLOCKED HERE
                #BLOCKED HERE
                newComment = Comments(session['user']['user_id'], comment, )

        return render_template("index.html", photo = photo, bio = bio, imgType = imgType, us = session['user']['user_name'])
    return render_template('index.html')

@app.route('/contact-us', methods=['GET', 'POST']) 
def contact(): 

    #form object, will be used for valida  tion and inserting parts into the html
    form = captchaForm(request.form)
    
    #check for a post request and see if the form is submitted and vailidated. (the last 2 are checked on validate_on_submit)
    if form.validate_on_submit() and request.method == "POST":
        issue = form.Issue.data #get the information from the textarea 
        #TODO put information from the issue into the database when tehre is a spot for it
        print(issue)
        
    #pass int he form object to the html page. ON the html side everything is loaded using Jinja2
    
    return render_template("contact.html", form=form)

@app.route('/sign-up', methods=['GET', 'POST']) 
def SignUp(): 

    message = ""
    username =" "
    password = ""
    confirmPass = ""
    email = ""
    if request.method == 'POST':
        #will have to connect this to the database when I have the file
        userName = request.form.get('userName', '')
        password = request.form.get('password', '')
        confirmPass = request.form.get('confirmPass', '')
        email = request.form.get('emailAddress', '')
        
        #if they leave a part blank then give the error
        if userName == '' or password == '' or confirmPass == '' or email == '':
            abort(400)
        if "@" not in email:
            abort(400)
        #if the 2 passwords they gave do not match give error
        if(password != confirmPass):
            abort(400)

        #if everything works, hash the password so it can be saved in the database
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')
            
        #create a user and add them to the database and commit the add. 
        newUser = Users(user_name = userName, passed = hashedPassword, email = email)
        db.session.add(newUser)
        db.session.commit()

    return render_template("create_account.html")

@app.route('/settings', methods=['GET','POST'])
def settings():
    return render_template("settings.html")

#route for login
@app.route('/sign-in', methods=['GET','POST']) 
def login():
    
    
    if request.method == 'POST':
        #get the information that the user input
        userName = request.form.get('userName')
        password = request.form.get('password')


        #input validation for the username and password for signin
        if userName == '' or password == '':
            abort(400)
        #make a user object with the user that was logged in
        user = Users.query.filter_by( user_name =userName).first()

        # if the user does not exist then cause error
        if not user or user.user_id == 0:
            return abort(400)
        # if the password does not match the one inputted then cause error
        if not bcrypt.check_password_hash(user.passed, password):
            return abort(400)
        
        #create the session for the user
        session['user'] = {
            'user_name': userName,
            'user_id': user.user_id
            }
        #this line will have to change when the home page is made because this is just validating the user is in the session. 
        return redirect("/")
    return render_template("login.html")

@app.route('/account', methods =['GET'])
def userAccount(username):
    #check for username in our Users table
    userAccount = Users.query.filter_by(username=Users.user_name).first()
    if userAccount is None: #if user is not found
        return redirect(url_for('sign-in')) #redirect them to the sign in page
    else:
        #grab their comment and post history
        comment_his = Users.query.get(Users.userAccount.comments)
        post_his = Users.query.get(Users.userAccount.posts)
        #TODOadd checks for if user clicks (account settings), render settings page
    return render_template("user_account.html", userAccount = userAccount, comment_his=comment_his, post_his=post_his )

@app.route('/new-post', methods=['GET', 'POST'])
def CreatePost(): 
    
    return render_template("create_post.html")

@app.get('/friends')
def search_users():
    found_users = []
    q = request.args.get('q', '')
    if q != '':
        found_users = users_repository_singleton.search_users(q)
    return render_template('friends.html', search_active=True, userlist=found_users, search_query=q)

if __name__ == '__main__':
    app.run()