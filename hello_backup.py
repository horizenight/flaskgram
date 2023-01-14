from flask import Flask ,render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm 
from wtforms import StringField , SubmitField , PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash

from datetime import date 
from wtforms.widgets import TextArea

from flask_login import UserMixin ,login_user ,LoginManager ,login_required,logout_user,current_user



#create a Flask Instance 
app = Flask(__name__)

#Add Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#secret Key ! 
app.config['SECRET_KEY'] ="hello"
app.debug = True

#initalise the databse 
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id): 
    return Users.query.get(int(user_id))


#Create a Login Form 
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create Login page
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            #check the hash 
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                flash('Yay Logged In!')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password - Try Again !')
        else:
            flash("User Doesnt Exist Try Again")
    return render_template('login.html',form=form)

#create Logout Page
@app.route('/logout',methods=['GET','POST'])
def logout():
    logout_user()
    flash("You have beeen logged Out !")
    return redirect(url_for('login'))



#Create Dashboard page
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id= current_user.id
    name_to_update = Users.query.get_or_404(id) 
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash('User Updated Successfully')
            return render_template('dashboard.html',form=form,name_to_update=name_to_update)
        except:
            flash('Try Again')
            return render_template('dashboard.html',form=form,name_to_update=name_to_update)

    else:
        return render_template('dashboard.html',form=form,name_to_update=name_to_update,id= id)






#Create a Blog Post Model
class Posts(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      title = db.Column(db.String(255))
      content = db.Column(db.Text)
      author=db.Column(db.String(255))
      date_posted=db.Column(db.DateTime,default =datetime.utcnow)
      img_url = db.Column(db.String(2083))
      slug= db.Column(db.String(255))


#Create a Post Form 
class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = StringField('Content',validators=[DataRequired()],widget=TextArea())
    author = StringField('Author',validators=[DataRequired()])
    img_url = StringField('Image URL')
    slug = StringField('Slug',validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html',post=post)









@app.route('/post/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        post.img_url = form.img_url.data

        #Update Datavbase
        db.session.add(post)
        db.session.commit()
        flash("Post has Been Updated !")
        return redirect(url_for('post',id=post.id))


    form.title.data = post.title
    form.author.data =post.author
    form.slug.data =post.slug
    form.content.data =post.content
    form.img_url.data = post.img_url

    return render_template('edit_post.html',form=form)

#add Posts Page
@app.route('/posts')
def posts():
    #Grab all the posts from the database 
    posts = Posts.query.order_by(Posts.date_posted) 
    return render_template("posts.html",posts=posts)


#delete post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()

        #Return a message
        flash("Blog Post Was Deleted")

        posts = Posts.query.order_by(Posts.date_posted) 
        return render_template("posts.html",posts=posts)
    except:
         flash("Whoops Try again")
         posts = Posts.query.order_by(Posts.date_posted) 
         return render_template("posts.html",posts=posts)





#add Post Page 
@app.route('/add/posts',methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            content = form.content.data,
            author=form.author.data,
            img_url = form.img_url.data,
            slug = form.slug.data
        )
        #clear the form
        form.title.data =''
        form.content.data=''
        form.author.data=''
        form.img_url.data=''
        form.slug.data=''

        #add post data to database 
        db.session.add(post)
        db.session.commit()


        flash("Blog Post Submitted Successfully")

    return render_template('add_post.html',form=form)





#Json Thing
@app.route('/date')
def get_current_date():
    return {"date": date.today()}




#create Model
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),nullable=False)
    name = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    #Do password 
    password_hash = db.Column(db.String(120))

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)




    #create a String 
    def __repr__(self):
        return '<Name %r>' % self.name 

#create a Form Class 
# CSFIR tokens 
class UserForm(FlaskForm):
    name = StringField("Name" , validators= [DataRequired()])
    username = StringField("UserName" , validators= [DataRequired()])
    email = StringField("Email" , validators= [DataRequired()])
    favorite_color = StringField('Favorite Color')
    password_hash = PasswordField('Password',validators=[DataRequired(),EqualTo('password_hash2',message='Passwords Must Match')])
    password_hash2 = PasswordField('Confirm Password',validators=[DataRequired()])

    submit = SubmitField("Submit")


@app.route('/delete/<int:id>')

def delete(id):

    name = None 
    form = UserForm()
    
    user_to_delete = Users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",form =  form,name=name,our_users = our_users)

    except:
        flash("User was not deleted")
        return render_template("add_user.html",form =  form,name=name,our_users = our_users)



#Update Database Record
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id) 
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash('User Updated Successfully')
            return render_template('update.html',form=form,name_to_update=name_to_update)
        except:
            flash('Try Again')
            return render_template('update.html',form=form,name_to_update=name_to_update)

    else:
        return render_template('update.html',form=form,name_to_update=name_to_update,id= id)

#create a Form Class 
# CSFIR tokens 
class NamerForm(FlaskForm):
    name = StringField("What's Your Name" , validators= [DataRequired()])
    submit = SubmitField("Submit")
# CSFIR tokens 
class PasswordForm(FlaskForm):
    email = StringField("What's Your Email" , validators= [DataRequired()])
    password_hash = PasswordField("What's Your Password" , validators= [DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add',methods =['GET',"POST"])
def add_user():
    name = None 
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data,"sha256")
            user = Users(username=form.username.data , name = form.name.data , email = form.email.data,favorite_color=form.favorite_color.data,password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data=''
        form.email.data=''
        form.username.data =''
        form.favorite_color=''
        form.password_hash=''
        flash("User Added Successfully")

    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",form =  form,name=name,our_users = our_users)

#create a route decorator 
@app.route('/')

#safe
#capitalize
#lower
#upper
#title
#trim 
#striptags



# def index():
#     return "<h1>Hello World<h1>"

def index():
    favorite_pizza = ['hello' , 'water ' , 'earth',41] 
    return render_template('index.html',favorite_pizza = favorite_pizza)



# localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
     return render_template('user.html' , user_name = name)


#Custom Error Pages

#Invalid URL 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
#Internal Server URL 
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500


#Create Name Page 
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #validation
    if form.validate_on_submit():

        name = form.name.data
        form.name.data =''
        flash("Form Submitted Successfully")

    return render_template('name.html',name = name , form = form)

#Create test_pw
@app.route('/test_pw',methods=['GET','POST'])
def test_pw():
    email = None
    password=None
    pw_to_check=None
    passed = None

    form = PasswordForm()
    #validation
    if form.validate_on_submit():

        email = form.email.data
        password = form.password_hash.data

        form.email.data =''
        form.password_hash.data =''

        pw_to_check = Users.query.filter_by(email=email).first()
        
        #check hashed Password 
        passed = check_password_hash(pw_to_check.password_hash , password)



        flash("Form Submitted Successfully")

    return render_template('test_pw.html',email= email,password=password ,pw_to_check = pw_to_check, form = form,passed = passed)