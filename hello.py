from flask import Flask ,render_template,flash,request,redirect,url_for

from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash

from datetime import date 


from flask_login import UserMixin ,login_user ,LoginManager ,login_required,logout_user,current_user


from WebForms import LoginForm,PostForm,UserForm,PasswordForm,NamerForm,SearchForm,Followforms

from sqlalchemy import MetaData
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from flask_ckeditor import CKEditor

from werkzeug.utils import secure_filename
import uuid as uuid 
import os 

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


metadata = MetaData(naming_convention=convention)


#create a Flask Instance 
app = Flask(__name__)

ckeditor = CKEditor(app)

#Add Database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#secret Key ! 
app.config['SECRET_KEY'] ="hello"
app.debug = True


UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#initalise the databse 
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app,db,render_as_batch=True)

#Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id): 
    return Users.query.get(int(user_id))



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
        name_to_update.about_author = request.form['about_author']
        # check for porfile pic 
        if request.files['profile_pic']:
            name_to_update.profile_pic = request.files['profile_pic']




            # grab Image name 
            pic_filename = secure_filename(name_to_update.profile_pic.filename)
            #set uuis 
            pic_name = str(uuid.uuid1())+"_"+pic_filename
            #save image name 
            saver = request.files['profile_pic']

            # change name to string
            name_to_update.profile_pic = pic_name

        
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
                flash('User Updated Successfully')
                return render_template('dashboard.html',form=form,name_to_update=name_to_update)
            except:
                flash('Try Again')
                return render_template('dashboard.html',form=form,name_to_update=name_to_update)
        else:
             db.session.commit()
             flash('User Updated Successfully')
             return render_template('dashboard.html',form=form,name_to_update=name_to_update)
             


    else:
        return render_template('dashboard.html',form=form,name_to_update=name_to_update,id= id)









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
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        post.img_url = form.img_url.data

        #Update Datavbase
        db.session.add(post)
        db.session.commit()
        flash("Post has Been Updated !")
        return redirect(url_for('post',id=post.id))

    if current_user.id == post.poster_id:
            
        form.title.data = post.title
        # form.author.data =post.author
        form.slug.data =post.slug
        form.content.data =post.content
        form.img_url.data = post.img_url
        return render_template('edit_post.html',form=form)
    else:
        flash("You arent authorized to edit this post!")
        return render_template('posts.html',posts=posts)


#add Posts Page
@app.route('/posts')
def posts():
    #Grab all the posts from the database 
    posts = Posts.query.order_by(Posts.date_posted) 
    return render_template("posts.html",posts=posts)


#delete post
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):

    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if(id == post_to_delete.poster.id):

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
    else:
            flash("You are not authorized to delete this post")
            posts = Posts.query.order_by(Posts.date_posted) 
            return render_template("posts.html",posts=posts)




#add Post Page 
@app.route('/add/posts',methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster=current_user.id
        post = Posts(
            title=form.title.data,
            content = form.content.data,
           poster_id = poster,
            img_url = form.img_url.data,
            slug = form.slug.data
        )
        #clear the form
        form.title.data =''
        form.content.data=''
        # form.author.data=''
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





@app.route('/delete/<int:id>')
@login_required
def delete(id):

    
    if id == current_user.id:
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
    else:
        flash("You are not authorised to delete")
        return redirect(url_for('dashboard'))


#Update Database Record
@app.route('/update/<int:id>',methods=['GET','POST'])
@login_required
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


# Create Admin Page
@app.route('/admin',methods=["GET","POSTS"])
@login_required
def admin():
    id = current_user.id
    if id == 1:
        return render_template("admin.html")
    else:
        flash("sorry you must be the admin to access this page")
        return redirect(url_for('dashboard'))




# pass stuff to navbaar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)



# #create a search function in posts
# @app.route('/search' , methods=["POST"])
# def search():
#     form = SearchForm()
#     posts = Posts.query
#     if form.validate_on_submit():
#         post.searched = form.searched.data
#         #QUERY THE Database
#         posts = posts.filter(Posts.content.like('%'+post.searched+'%'))
#         posts = posts.order_by(Posts.title).all()

#         return render_template("search.html",form = form, searched = post.searched,posts=posts)
  
    

#create a search function  in users
@app.route('/search' , methods=["POST"])
def search():
    form = SearchForm()
    users = Users.query
    posts = Posts.query
    
    if form.validate_on_submit():
        user.searched = form.searched.data
        post.searched = form.searched.data
        
        #QUERY THE Database
        users = users.filter(Users.username.like('%'+user.searched+'%'))
        users = users.order_by(Users.username).all()
        
         #QUERY THE Database
        posts = posts.filter(Posts.content.like('%'+post.searched+'%'))
        posts = posts.order_by(Posts.title).all()


        # return render_template("search.html",form = form, searched = post.searched,posts=posts)
        return render_template("search.html" , form = form , searched = user.searched , users = users,posts=posts)
  
    





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



# UserProfile
@app.route('/user/<username>')
def user(username):
    user = Users.query.filter_by(username=username).first()
    
    return render_template('user.html' ,user=user, username = username)



# Followers implementation 


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = Followforms()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = Followforms()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))



@app.route('/feed/<username>', methods=["GET"])
@login_required
def feed(username):
    user = Users.query.filter_by(username=username).first()
    # we have grabed user 
    posts = user.followed_posts()
    return render_template("posts.html",posts=posts)



# @app.route('/add/comment',methods=["POST"])
# def add_comment(id):
#     comment = Comment(text="Hello world" , author = current_user.username)

#     try:
#         db.session.add(comment)
#         db.session.commit()
#         flash("Comment posted")
#     except:
#         flash("Comment not posted")






#Classes




#Create a Blog Post Model
class Posts(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      title = db.Column(db.String(255))
      content = db.Column(db.Text)
      #author=db.Column(db.String(255))
      date_posted=db.Column(db.DateTime() ,default =datetime.utcnow)
      img_url = db.Column(db.String(2083))
      slug= db.Column(db.String(255))
      #Foreign Key to Link Users (refer to primary)
      poster_id = db.Column(db.Integer,db.ForeignKey("users.id"))




# Create followers 
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)



# #Create Comment 
# class Comment(db.Model):
#     id = db.Column(db.Model);
#     text = db.Column(db.String(140))
#     author = db.Column(db.String(32))
#     date_posted=db.Column(db.DateTime() ,default =datetime.utcnow,index=True)
#     parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
#     replies = db.relationship(
#         'Comment', backref=db.backref('parent', remote_side=[id]),
#         lazy='dynamic')









#create Model
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),nullable=False)
    name = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    profile_pic = db.Column(db.String(),nullable=True)
    favorite_color = db.Column(db.String(120))
    about_author = db.Column(db.Text(500),nullable=True)
    date_added = db.Column(db.DateTime,default=datetime.utcnow)
    #Do password 
    password_hash = db.Column(db.String(120))

    #Users can have many posts
    posts= db.relationship('Posts',backref='poster')
    #followed relationship
    followed = db.relationship(
        'Users', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)
    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id == user.id).count()>0

    def followed_posts(self):
        followed= Posts.query.join(
            followers,(followers.c.followed_id == Posts.poster_id)).filter(
                followers.c.follower_id == self.id
            )
        own = Posts.query.filter_by(poster_id = self.id)
        return followed.union(own).order_by(Posts.date_posted.desc())


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
