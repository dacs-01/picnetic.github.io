

import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, abort, url_for
#imports for the recaptcha
from form import captchaForm
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt



app = Flask(__name__)

bcrypt = Bcrypt(app)
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
#ISSUE WITH THIS LINE HERE RIGHT HERE
#recaptcha = RecaptchaField() # Create a ReCaptcha obejct with the app as the parameter. 


@app.route('/', methods=['GET', 'POST']) 
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

@app.route('/home', methods=['GET', 'POST']) 
def SigtnUp(): 
    message = ""
    if request.method == 'POST':
        userName = request.form.get('userName')
        password = request.form.get('password')
        confirmPass = request.form.get('confirmPass')
        email = request.form.get('emailAddress')
        
        if userName == '' or password == '' or confirmPass == '' or email == '':
            abort(400)
        if(password != confirmPass):
            message = "Your passwords did not match. Try again."
            abort(400)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
    message = ""
    return render_template("create_account.html", message = message)


if __name__ == '__main__':
    app.run()