#form file for recaptcha contact page. This deals with some basic css forms and helps with user input validation. 
#import the flask form and the Recaptcha Field
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import  PasswordField, TextAreaField, StringField, validators

class captchaForm(FlaskForm):   
    #custom css for the textfield because it is inserted through flask and not just in HTML
    customTextArea = {'style':"width: 38%; height: 25%; margin-bottom: 50px; margin-top: 50px;", 'class':"form-control", 'placeholder':"Description"}
    
    #a textarea that has a max of 255 characters. and the custom CSS elements created from above. This will be put into the page.
    Issue = TextAreaField('Issue', [validators.DataRequired(), validators.Length(max=255)], render_kw= customTextArea    )
    recaptcha = RecaptchaField() #the recaptcha that is going to be in the HTML for the users to click