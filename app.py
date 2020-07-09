from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
import json
# from datetime import datetime
with open('config.json', 'r') as c:
    params = json.load(c)["params"]
    
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/anuj'

db = SQLAlchemy(app)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(12), nullable=False)


class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(12), nullable=True)

@app.route('/')
def hello():
    posts = Posts.query.filter_by().all()[0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/anuj/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
     print(post_slug)
     post = Posts.query.filter_by(slug=post_slug).first()
     return render_template('post.html', params=params,post=post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if(request.method=='POST'):
       
        user_name = request.form.get('name')
        phone = request.form.get('phone')
       
        entry = Info(name=user_name, mobile = phone )
        db.session.add(entry)
        db.session.commit()
        
    return render_template('contact.html')


app.run(debug=True)