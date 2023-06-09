#------------------------------------------------------------------------------------------------------------------------------------------                            _
# (_)                          | |
# _ _ __ ___  _ __   ___  _ __| |_ ___
# | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
# | | | | | | | |_) | (_) | |  | |_\__ \
# |_|_| |_| |_| .__/ \___/|_|   \__|___/
#           | |
#           |_|
import os
from re import I
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, abort, url_for, session, url_for, flash, send_from_directory
from sqlalchemy import null
# imports for the recaptcha
from form import captchaForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from src.models import db, Users, Comments, Post, Contact
import base64
import io
from src.repositories.users_repository import users_repository_singleton
from werkzeug.utils import secure_filename
import requests
import html
# ------------------------------------------------------------------------------------------------------------------------------------------

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(app.config['UPLOAD_FOLDER'])
bcrypt = Bcrypt(app)
# ------------------------------------------------------------------------------------------------------------------------------------------
#                                          __ _                       _   _
#     /\                                  / _(_)                     | | (_)
#    /  \   _ __  _ __     ___ ___  _ __ | |_ _  __ _ _   _ _ __ __ _| |_ _  ___  _ __
#   / /\ \ | '_ \| '_ \   / __/ _ \| '_ \|  _| |/ _` | | | | '__/ _` | __| |/ _ \| '_ \
#  / ____ \| |_) | |_) | | (_| (_) | | | | | | | (_| | |_| | | | (_| | |_| | (_) | | | |
# /_/    \_\ .__/| .__/   \___\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__|_|\___/|_| |_|
#          | |   | |                             __/ |                                  (keys and things)
#          |_|   |_|                            |___/
# 2 recaptcha keys. The site key and then the site secret key.
# if you want to make your own:  got to the https://developers.google.com/recaptcha/intro and click on "sing up for an API key pair"
# from there, you create a website and make sure to click reCaptcha v2. For domains, put down the 127.0.0.1 and localhost as the domains.
# For secuirty preference, I put it in the middle between easiest and most secure
# when you click save, it should give you your 2 keys which you will then put in the .env file.
# it might take a few days for you to get the recaptcha information in the analytics center.
RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")
APP_SECRET = os.environ.get("APP_SECRET")

# the secret key for the flask site. Makes sure sessions are protected. I generated a random key using os.urandom()
app.config['SECRET_KEY'] = APP_SECRET
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY
# ------------------------------------------------------------------------------------------------------------------------------------------


# This is the dotenv connection string for our database
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLEARDB_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
picFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/', methods=['GET', 'POST'])
def index():
    # Query all of the items from each table for sending in later
    posts = Post.query.all()
    comments = Comments.query.all()
    users = Users.query.all()
    print(posts)
    post1 = "hi"

    if posts != []:
        post1 = posts[0]

    formNum = 0
    hi = ""
    # check if the user is in the session
    if 'user' in session:
        # if the user makes a post request
        if request.method == 'POST':

            # get the comment
            comment = ""
            # get the post id that the comment was made on. I have to do this because the modal doesn't make a get request to a certain page
            for i in range(len(posts)):
                id = posts[i].post_id

                if request.form['post'] == str(id):
                    formNum = id
                    comment = request.form.get('comment')

            # check if the comment is real create the comment
            if comment != '':
                newComment = Comments(user_id=int(
                    session['user']['user_id']), comment=comment, post_id=int(formNum))
                db.session.add(newComment)
                db.session.commit()
                return redirect(f'/comment/{newComment.comment_id}')
        return render_template("index.html", us=session['user']['user_name'], posts=posts, comments=comments, users=users, ui=session['user']['user_id'])
    return redirect("/sign-up")


@app.route('/contact-us', methods=['GET', 'POST'])
def contact():

    # form object, will be used for valida  tion and inserting parts into the html
    form = captchaForm(request.form)

    # check for a post request and see if the form is submitted and vailidated. (the last 2 are checked on validate_on_submit)
    if form.validate_on_submit() and request.method == "POST":
        issue = form.Issue.data  # get the information from the textarea

        contact_id = session['user']['user_id']
        userMail = Users.query.get(contact_id)

        newIssue = Contact(user_id=contact_id, email=userMail, description=issue)
        db.session.add(newIssue)
        db.session.commit()

        return redirect('/')
    # pass int he form object to the html page. ON the html side everything is loaded using Jinja2

    return render_template("contact.html", form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def SignUp():

    message = ""
    username = " "
    password = ""
    confirmPass = ""
    email = ""
    if request.method == 'POST':
        # will have to connect this to the database when I have the file
        userName = request.form.get('userName', '')
        password = request.form.get('password', '')
        confirmPass = request.form.get('confirmPass', '')
        email = request.form.get('emailAddress', '')

        # if they leave a part blank then give the error
        if userName == '' or password == '' or confirmPass == '' or email == '':
            abort(400)
        if "@" not in email:
            abort(400)
        # if the 2 passwords they gave do not match give error
        if(password != confirmPass):
            abort(400)

        # if everything works, hash the password so it can be saved in the database
        hashedPassword = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # create a user and add them to the database and commit the add.
        newUser = Users(user_name=userName, passed=hashedPassword, email=email)
        db.session.add(newUser)
        db.session.commit()

    return render_template("create_account.html")


@app.route('/settings/<user_id>', methods=['GET', 'POST'])
def settings(user_id):
    if 'user' in session:

        userAccount = Users.query.get(user_id)
        fname = request.form.get('fname','')
        lname = request.form.get('lname','')
        email = request.form.get('email', '')

        if email == '':
            email = userAccount.email
        if fname == '':
            fname = userAccount.f_name
        if lname == '':
            lname = userAccount.l_name
            
        userAccount.f_name = fname
        userAccount.l_name = lname
        userAccount.email = email

        db.session.commit()
        return render_template("settings.html")


    return render_template("settings.html",  ui = session['user']['user_id'] )

# route for login


@app.route('/sign-in', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        # get the information that the user input
        userName = request.form.get('userName')
        password = request.form.get('password')

        # input validation for the username and password for signin
        if userName == '' or password == '':
            abort(400)
        # make a user object with the user that was logged in
        user = Users.query.filter_by(user_name=userName).first()

        # if the user does not exist then cause error
        if not user or user.user_id == 0:
            return abort(400)
        # if the password does not match the one inputted then cause error
        if not bcrypt.check_password_hash(user.passed, password):
            return abort(400)

        # create the session for the user
        session['user'] = {
            'user_name': userName,
            'user_id': user.user_id
        }

        # this line will have to change when the home page is made because this is just validating the user is in the session.
        return redirect("/")
    return render_template("login.html")


@app.route('/account/<user_id>', methods=['GET'])
def userAccount(user_id):
    if 'user' in session:
        userid = session['user']['user_id']
    # check for username in our Users table
        userAccount = Users.query.get(userid)
        comment_his = userAccount.comments
        post_his = userAccount.posts

        if comment_his and post_his is None:
            return render_template("account2.html", userAccount=userAccount)

    return render_template("account.html", userAccount=userAccount, comment_his=comment_his, post_his=post_his, ui = session['user']['user_id'])


def is_allowed(filename):
    # cut the filename  at the .
    wordList = filename.split(".")
    # check if teh extension is corerect. (uses -1 just in case there is a period in the filename for some reason)
    if wordList[-1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


@app.route('/new-post', methods=['POST', 'GET'])
def CreatePost():
    if 'user' in session:

        print(session['user']['user_name'])
        if request.method == 'POST':

            # get the file.
            image = request.files['file']
            # if no file was uploaeded then send an error
            if image.filename == "":
                abort(404)
            # check if the file is supported and an image
            if image and is_allowed(image.filename):
                imageName = secure_filename(image.filename)
                # save the image in the upload folder.
                image.save(os.path.join(
                    app.config['UPLOAD_FOLDER'], imageName))
                imageURL = url_for('uploaded_file', filename=imageName)

            label = request.form.get('post-label')
            print(label)
            cap = request.form.get('caption')
            imageURL = str(imageURL)

            post = Post(user_id=session['user']['user_id'], post_label=label,
                        post_cap=cap, post_picture=imageURL)  # Add Username

            db.session.add(post)
            db.session.commit()

            print(post)

            return get_post(post.post_id)
    return render_template("bruv.html")


# route that makes an image a link
@app.route('/static/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/<post_id>')
def get_post(post_id):
    # get all of the needed code.
    post = Post.query.get_or_404(post_id)
    comments = Comments.query.all()
    users = Users.query.all()


    # NEED TO ADD WAY TO COMMENT HERE AND THEN DO THE BUTTON TO EDIT/DELETE POST AS WELL. NOT 100% but can be soon. WAnt to finish my current page
    return render_template("singlepost.html", post=post, us=session['user']['user_id'], comments=comments)


@app.route('/post/<post_id>/edit')
def edit_post(post_id):
    post = Post.query.get(post_id)
    if session['user']['user_id'] == post.user_id:
        return render_template("edit.html", post=post)
    else:
        abort(400)


@app.post('/<post_id>')
def update_post(post_id):
    updatePost = Post.query.get(post_id)
    type = request.form.get('post-label', '')
    caption = request.form.get('caption', '')

    if type == "none":
        type = updatePost.post_label
    if caption == '':
        caption = updatePost.post_cap

    updatePost.post_cap = caption
    updatePost.post_label = type

    db.session.commit()

    return redirect(f'/{post_id}')

# delete post and all comments related to the post


@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    # get the post comments
    post = Post.query.get(post_id)

    if session['user']['user_id'] == post.user_id:

        comments = Comments.query.all()
        # make sure the comment relates to the post being deleted and delete them
        for c in comments:
            if c.post_id == post.post_id:
                db.session.delete(c)
                db.session.commit()
        # make sure the user can delete the post. If they can then delte the post

        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    else:
        abort(400)


@app.route('/comment/<comment_id>')
def get_comment(comment_id):
    # get all of the needed code.
    if 'user' in session:
        comment = Comments.query.get(comment_id)
        users = Users.query.all()

        return render_template("singleComment.html", us=session['user']['user_name'], comment=comment, ui=session['user']['user_id'])


@app.route('/comment/<comment_id>/edit')
def edit_comment(comment_id):
    comment = Comments.query.get(comment_id)
    if session['user']['user_id'] == comment.user_id:
        return render_template("editComment.html", comment=comment)
    else:
        abort(400)


@app.post('/comment/<comment_id>')
def upadate_comment(comment_id):
    # get teh comment
    updateComment = Comments.query.get(comment_id)
    # get the new comment the person typed in
    comment = request.form.get('comment', '')
    # if it is blank then leave it the same
    if comment == '':
        comment = updateComment.comment
    # update the comment
    updateComment.comment = comment
    # commit the update
    db.session.commit()
    return redirect(f'/comment/{comment_id}')


@app.route('/comment/<comment_id>/delete', methods=["POST"])
def delete_comment(comment_id):
    # get the comment
    comment = Comments.query.get(comment_id)
# check if the user ownns teh comment
    if session['user']['user_id'] == comment.user_id:

        # make sure the user can delete the comment. If they can then comment the post
        db.session.delete(comment)
        db.session.commit()
        return redirect('/')
    else:
        abort(400)


@app.get('/search-users')
def search_users():
    # creates empty array to store users
    found_users = []
    q = request.args.get('q', '')
    # if the query is not empty searches the db for the user
    if q != '':
        found_users = users_repository_singleton.search_users(q)
    # return a template with the list of users found
    return render_template('user_search.html', search_active=True, userlist=found_users, search_query=q)


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.route('/delete/<user_id>', methods=['POST'])
def delete(user_id):
    if 'user' in session:
        userid = session['user']['user_id']
        userAccount = Users.query.get(userid)
        if request.method == 'POST':
            # delete users comments
            comment_his = userAccount.comments
            for c in comment_his:
                db.session.delete(c)
            # delete users posts
            post_his = userAccount.posts
            for p in post_his:
                db.session.delete(p)    
            # finally, delete the user's account
            db.session.delete(userAccount)
            db.session.commit()
    return render_template('deletedAccount.html')
#logout
@app.post('/logout')
def logout():
    #make sure user is in session log them out
    if 'user'  in session:
        del session['user']

    return redirect('/')


if __name__ == '__main__':
    app.run()
