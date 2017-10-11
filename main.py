from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 
from pprint import pprint
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text())

    def __init__(self, name):
        self.name = name

entries = []

@app.route('/blog', methods=['GET'])
def index():
    entries = Blog.query.all()
    
    return render_template('blog.html', title='My Blog', blogs=entries)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        entry = Blog('blog')
        entry.title = request.form['title']
        entry.body = request.form['body']
        db.session.add(entry)
        db.session.commit()

        return redirect('/blog', code=302)
    
    return render_template('newblog.html', title="New Blog Post")

if __name__ == '__main__':
    app.run()