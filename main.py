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
    if 'id' in request.args: 
        id = request.args['id']
        entry = Blog.query.filter_by(id=id).first()
        return render_template('singleblog.html', title=entry.title, blog=entry)
     
    entries = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', title='My Blog', blogs=entries)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if request.method == 'POST':
        entry = Blog('blog')
        entry.title = request.form['title']
        entry.body = request.form['body']

        if entry.title == '':
            return render_template('newblog.html', title="New Blog Post", form=request.form, errorMessage="Title is required")

        if entry.body == '':
            return render_template('newblog.html', title="New Blog Post", form=request.form, errorMessage="Body is requried")

        db.session.add(entry)
        db.session.commit()

        return redirect('/blog?id=' + str(entry.id), code=302)
    
    return render_template('newblog.html', title="New Blog Post", form=[])

if __name__ == '__main__':
    app.run()