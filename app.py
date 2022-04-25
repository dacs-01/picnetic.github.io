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
from flask import Flask, redirect, render_template, request, abort, url_for
#imports for the recaptcha
from form import captchaForm
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from src.models import db
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

#the secret key for the flask site. Makes sure sessions are protected. I generated a random key using os.urandom()
app.config['SECRET_KEY'] = os.urandom(15)
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
#------------------------------------------------------------------------------------------------------------------------------------------

#This is the dotenv connection string for our database
load_dotenv()

db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('BD_PORT', '3306')
db_user = os.getenv('DB_USER', 'root')
db_pass = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME', 'picnetic_db')

connection_string = f'mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/', methods =['GET'])
def index():
    return render_template("index.html")

@app.route('/contact-us', methods=['GET', 'POST']) 
def contact(): 

    #form object, will be used for validation and inserting parts into the html
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
    if request.method == 'POST':
        #will have to connect this to the database when I have the file
        userName = request.form.get('userName')
        password = request.form.get('password')
        confirmPass = request.form.get('confirmPass')
        email = request.form.get('emailAddress')
        
        #if they leave a part blank then give the error
        if userName == '' or password == '' or confirmPass == '' or email == '':
            abort(400)

        #if the 2 passwords they gave do not match give error
        if(password != confirmPass):
            abort(400)

        #if everything works, hash the password so it can be saved in the database
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            

    #TODO use the hased password, email, and username to create a new user. Can be done when we have a models file.
    #
    return render_template("create_account.html")

@app.route('/settings', methods=['GET','POST'])
def settings():
    return render_template("settings.html")

@app.route('/new-post', methods=['GET', 'POST'])
def CreatePost(): 
    
    return render_template("create_post.html")

if __name__ == '__main__':
    app.run()