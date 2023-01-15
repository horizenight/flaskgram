# Flaskgram 
A Instagram Blog application clone made using flask and sqlite database 



# Deployed Link Valid upto 15th april 2023 
[FlaskGram](http://horizenight.pythonanywhere.com/posts)

## Installation instruction
### 1. run command

pip install -r "requirements.txt"

### 2. Run 
flask --app main --debug run 
to run the flask app 


# Details:

### `     `Author
**Kshitij Roodkee** 

I am a web enthusiast and open source contirubutor who is excited to learn coding.
### Description

This project gives us hand on experience on the working of flask and databases to create a web app the keypoints to learn was using queries , passing data in flask .
### Technologies used
1. **Jinja2 :** It is a tempelating engine which gives us power to use python in html 
1. **WTForms :** it is used to validate and build forms that are more secure and easy to use.
1. **Werkzeug :** It is used to enhance login security and save the user password as hashes
1. **SQLAlchemy :** It is used to work with queries on a sqlite database 
1. **flask\_ckeditor :** To give a rich editing experience while writing the blog 
1. **Flask\_login :** It is used to implement login and logout feature.
1. **Flask :**  It is a web framework .
### DB Schema Design


![Screenshot 2023-01-15 233238](https://user-images.githubusercontent.com/76839614/212563633-46030193-6de4-4f35-ac95-244435a6cd77.png)

### `    `Architecture and Features

The project architecture could be divided into 

1. **Templates** : It contains all the views/html files 
1. **Static Folder** : It contains Css and images folder ( user profile picture)
1. **Routes :** Their are mainly 
   1. “/posts” route: which shows all the post available in the database
   1. “/feed/<username>” route  which shows specific post depending upon if user follows that author or not 
   1. “/add/posts” route: for adding blog post 
   1. “/user/<username>” route: shows user profile and stats
   1. “/follower/<username>” route: shows user followers list
   1. “/following/<username>” route : shows user following list
   1. “/user/dashboard” route: shows user setting can be used to update user profile setting here 
   1. “/posts/edit/<id>” route: for editing posts
   1. “/posts/delete/<id> route: for removing posts
1. **Classes** :Their are three classes or model implemented	
   1. Posts : to maintain Posts 
   1. Users : to maintain Users
   1. LikePost  : to maintain likes on the post
1. **Forms :** The forms are main feature to get the user input: The different forms implemented are:	
   1. LoginForm : To be used for login 
   1. SearchForm : To implement Search Functionality 
   1. FollowForm:  To submit follow request


**Features Implemented :** 

1. **Users Customised Feed :** A user is able to create his/her own feed by determining whom to follow . This feature is implemented using by creating a relationship between users Many to Many and querying on this relationship.
1. **Likes :** A user can determine the credibility of a post bhy seeing the likes . This feature is implemented by creating a db model that keeps in count the no. of likes on that post
1. **Archive :** A user can archive a post or unarchive a post depending upon his/her needs. This feature is implemented using a check of 0 and 1 count associated with the post where 1 means archived and 0 means unarchived.
1. **Login and Logout:**  Access to pages are maintained . A user can only see global posts if he/she is not logged in . Rest all pages need to be logged in . It is implemented using flask\_login module.
1. **Search :** A user is able to search another user and also able to search post content. This is implemented using simple query on db
1. **Follow and Unfollow:** A user is able to follow unfollow another user . This is implemented using function call and a relationship between users .




