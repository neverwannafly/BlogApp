from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd())+"/blog.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

# Video (Layout) -> 
#     _API_KEY = "AIzaSyAr78B7PUvpUqXlHsBAL8kEd3BRNOp6aEw" -> 0
#     view_count = "" -> 1
#     like_count = "" -> 2
#     dislike_count = "" -> 3
#     favourite_count = "" -> 4
#     comment_count = "" -> 5
#     url = "" -> 6
# , default=",,,,,"

# Location_Manager (Layout) ->
#     _API_KEY = "AIzaSyB1hPDbNRwBqg-msjWUq7anQOW4IynsP7M" -> 0
#     latitude = "" -> 1
#     longitude = "" -> 2
#     accuracy = "" -> 3 , default=",,"


# Defines the Post model which would be displayed on the website!
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

@app.route('/test')
def test():
    posts = Post.query.all()
    post_details = [post.returnObject() for post in posts]
    return jsonify({'posts': post_details, 'total': len(post_details)})

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(unique_id=post_id).one()
    date_posted = post.timestamp.strftime('%B %d, %Y')
    return render_template('post.html', post=post, date_posted=date_posted)

@app.route('/add')
def add():
    return render_template('add.html')

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