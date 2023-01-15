
from flask_wtf import FlaskForm 
from wtforms import StringField , SubmitField , PasswordField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,EqualTo,Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

#Create a Login Form 
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create a SearchForm
class SearchForm(FlaskForm):
    searched = StringField("Searched" , validators=[DataRequired(),Length(min=1)])
    submit = SubmitField("Submit")




#Create a Post Form 
class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    # content = StringField('Content',validators=[DataRequired()],widget=TextArea())
    content = CKEditorField('Content',validators=[DataRequired()])
    author = StringField('Author')
    img_url = StringField('Image URL')
    slug = StringField('Slug',validators=[DataRequired()])
    submit = SubmitField('Submit')


    #create a Form Class 
# CSFIR tokens 
class UserForm(FlaskForm):
    name = StringField("Name" , validators= [DataRequired()])
    username = StringField("UserName" , validators= [DataRequired()])
    email = StringField("Email" , validators= [DataRequired()])
    favorite_color = StringField('Favorite Color')
    about_author = TextAreaField('About Author')
    profile_pic = FileField("Profile Pic")
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must Match')])
    password_hash2 = PasswordField('Confirm Password',validators=[DataRequired()])

    submit = SubmitField("Submit")




class Followforms(FlaskForm):
    submit = SubmitField('Submit')

