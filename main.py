from flask import Flask, request, redirect, render_template, session #we wanna have access to all of these
from flask_sqlalchemy import SQLAlchemy 
from pprint import pprint
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app = Flask(__name__) #create a flask object
app.config['DEBUG'] = True #setting the values for the flask object
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@127.0.0.1:8889/blogz' #this connects to the database
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key="Hello"

db = SQLAlchemy(app) #we are creating a SQLAlchemy object and storing it in the db

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())
    owner_id= db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, name, owner): #default function that gets called when a class is created
        self.name = name
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="user")

    def __init__(self, name):
        self.name = name

entries = []
@app.route('/user', methods=['GET'])  # decorator knows that the following lines is 
#what it would call if the decorator matched. # if the app. route '/' or whatever else I
# might have there and if it matched the post or get, it owuld run the code below. GET retrieve info, POST send info
def userpage():
    if 'id' in request.args: 
        id = request.args['id']
        user = User.query.filter_by(id=id).first()
        return render_template('singleUser.html', user=user)

    return redirect("/")


@app.route('/blog', methods=['GET'])
def blog():
    if 'id' in request.args: 
        id = request.args['id']
        entry = Blog.query.filter_by(id=id).first()
        return render_template('singleblog.html', title=entry.title, blog=entry)
     
    entries = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', title='My Blog', blogs=entries)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        #find the user that was submitted
        if request.form['pwd-verify'] != request.form['pwd']:
            return render_template('signup.html', form=request.form, errorMessage="Passwords do not match")

        if len(request.form['username']) < 3:
            return render_template('signup.html', form=request.form, errorMessage="Username must have more than 3 characters")

        if len(request.form['pwd']) < 3:
            return render_template('signup.html', form=request.form, errorMessage="Passwords must have more than 3 characters")
        
        username=request.form['username']
        user=User.query.filter_by(username=username).first()
        if user is not None:
            return render_template('signup.html', form=request.form, errorMessage="Username already exists")
            
        user=User('user')
        user.username=request.form['username']
        user.password=request.form['pwd']

        #if user.username == '':
        #    return render_template('signup.html', form=request.form, errorMessage="Username is required")

        #if user.password == '':
        #    return render_template('signup.html', form=request.form, errorMessage="Password is required")

        db.session.add(user)
        db.session.commit()
        return redirect('/newpost', code=302)
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST': #we should receive username and pwd
        username=request.form['username']
        password=request.form['pwd']

        #find the user that was submitted
        user=User.query.filter_by(username=username).first()

        #we need to check the password is correct
        if user.password==password:
            session["Username"]=user.username
            return redirect('/newpost', code=302)
        else: 
            return render_template ('login.html')#todo add warning for incorrect password
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    #todo need to clear the username from the session
    del session["Username"]
    return redirect('/blog')

@app.route('/', methods=['GET'])
def index():
    users=User.query.all() #with this you can query all rows of the Task table
    return render_template('index.html',users=users)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        user = User.query.filter_by(username=session['Username']).first()
        entry = Blog('blog', user)
        entry.title = request.form['title']
        entry.body = request.form['body']
        entry.password = request.form['password']
        entry.owner_id = user.id

        if entry.title == '':
            return render_template('newblog.html', title="New Blog Post", form=request.form, errorMessage="Title is required")

        if entry.body == '':
            return render_template('newblog.html', title="New Blog Post", form=request.form, errorMessage="Body is required")
    
        
        db.session.add(entry)
        db.session.commit()

        return redirect('/blog?id=' + str(entry.id), code=302)
    
    return render_template('newblog.html', title="New Blog Post", form=[])

if __name__ == '__main__':
    app.run()


