from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd())+"/blog.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

class Post(db.Model):
    unique_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    name_of_party = db.Column(db.String(100))
    image = db.Column(db.String(200))
    upvote_counter = db.Column(db.Integer)
    downvote_counter = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)
    location = db.Column(db.String(500))
    video = db.Column(db.String(500))
    
    def returnObject(self):
        self.location = self.location.split(",")
        self.video = self.video.split(",")

        if len(self.location) != 3:
            self.location = ",,,"
        if len(self.video) != 6:
            self.video = ",,,,,,"

        return {
            "unique_id" : self.unique_id,
            "title" : self.title,
            "name_of_party" : self.name_of_party,
            "content" : self.content,
            "upvote_counter" : self.upvote_counter,
            "downvote_counter" : self.downvote_counter,
            "timestamp" : self.timestamp,
            "location" : {
                "latitude" : self.location[0],
                "longitude" : self.location[1],
                "accuracy" : self.location[2],
            },
            "video" : {
                "view_count" : self.video[0],
                "like_count" : self.video[1],
                "dislike_count" : self.video[2],
                "favourite_count" : self.video[3],
                "comment_count" : self.video[4],
                "url" : self.video[5],
            }
        }

@app.route('/admin/test')
def test():
    posts = Post.query.all()
    post_details = [post.returnObject() for post in posts]
    return jsonify({'posts': post_details, 'total': len(post_details)})

@app.route('/')
@app.route('/home')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/filter/by/location/<location>')
def index_location_filter(location):
    posts = Post.query.filter_by(location=location).all()
    return render_template('index.html', posts=posts)

@app.route('/filter/by/name_of_party/<name_of_party>')
def index_party_name_filter(name_of_party):
    posts = Post.query.filter_by(name_of_party=name_of_party).all()
    return render_template('index.html', posts=posts)

@app.route('/filter/by/name_of_party')
def party_bridge_view():
    posts = db.session.query(Post.name_of_party.distinct().label("name_of_party"))
    return render_template('party_bridge.html', posts=posts)

@app.route('/filter/by/location')
def location_bridge_view():
    posts = db.session.query(Post.location.distinct().label("location"))
    return render_template('location_bridge.html', posts=posts)

@app.route('/sort/by/timestamp/')
def index_timestamp_sort():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)
    
@app.route('/sort/by/upvote_counter/')
def index_upvote_counter_sort():
    posts = Post.query.order_by(Post.upvote_counter.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(unique_id=post_id).one()
    date_posted = post.timestamp.strftime('%B %d, %Y')
    return render_template('post.html', post=post, date_posted=date_posted)

@app.route('/post/<int:post_id>/upvote')
def upvote_post(post_id):
    post = Post.query.filter_by(unique_id=post_id).one()
    post.upvote_counter += 1
    db.session.commit()
    date_posted = post.timestamp.strftime('%B %d, %Y')
    return render_template('post.html', post=post, date_posted=date_posted)

@app.route('/post/<int:post_id>/downvote')
def downvote_post(post_id):
    post = Post.query.filter_by(unique_id=post_id).one()
    post.downvote_counter += 1
    db.session.commit()
    date_posted = post.timestamp.strftime('%B %d, %Y')
    return render_template('post.html', post=post, date_posted=date_posted)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/post/delete/<int:post_id>')
def deletepost(post_id):
    post = Post.query.filter_by(unique_id=post_id).one()
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/addpost', methods=["POST"])
def addpost():
    title = request.form['title']
    name_of_party = request.form['name_of_party']
    image = request.form['image']
    location = request.form['location']
    video = request.form['video']
    content = request.form['content']

    # Set getVideo and getLocation methods here and use string interpolation to send them back!

    location = ",,"
    video = ",,,,,"

    post = Post(
        title=title,
        name_of_party = name_of_party,
        image = image,
        location = location,
        video = video,
        content = content,
        timestamp = datetime.now(),
        upvote_counter = 0,
        downvote_counter = 0
    )
 
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)