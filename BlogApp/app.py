from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from markupsafe import Markup

import requests
import os

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd())+"/blog.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

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
        video = self.video.split(",")

        if len(video) != 5:
            video = ",,,,,,"

        return {
            "image" : self.image,
            "unique_id" : self.unique_id,
            "title" : self.title,
            "name_of_party" : self.name_of_party,
            "content" : self.content,
            "upvote_counter" : self.upvote_counter,
            "downvote_counter" : self.downvote_counter,
            "timestamp" : self.timestamp,
            "location" : self.location,
            "video" : {
                "view_count" : video[0],
                "like_count" : video[1],
                "dislike_count" : video[2],
                "favourite_count" : video[3],
                "url" : video[4],
            }
        }

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/admin/login', methods=["GET", "POST"])
def admin_login():
    return render_template('admin_login.html')
    
@app.route('/admin/test')
def test():
    posts = Post.query.all()
    post_details = [post.returnObject() for post in posts]
    return jsonify({'posts': post_details, 'total': len(post_details)})

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

    # Location Autocomplete

    search = location
    location_response = requests.get("https://maps.googleapis.com/maps/api/place/autocomplete/json?input="+search+"&types=(cities)&key=AIzaSyB1hPDbNRwBqg-msjWUq7anQOW4IynsP7M")
    location_response = location_response.json()
    location = location_response['predictions'][0]['description']

    print(location)

    # Video Manager

    video_id = video[32:]
    response = requests.get('https://www.googleapis.com/youtube/v3/videos?part=statistics&id=' + video_id + '&key=AIzaSyAr78B7PUvpUqXlHsBAL8kEd3BRNOp6aEw')

    response_json = response.json()
    view_count = response_json['items'][0]['statistics']['viewCount']
    like_count = response_json['items'][0]['statistics']['likeCount']
    dislike_count = response_json['items'][0]['statistics']['dislikeCount']
    favourite_count = response_json['items'][0]['statistics']['favoriteCount']

    video = video[:24] + "embed/" + video[32:]
    video = video + "," + view_count + "," + like_count + "," + dislike_count + "," + favourite_count

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

@app.route('/analytics')
def analytics():
    posts = db.session.query(Post.name_of_party.distinct().label("name_of_party"))
    return render_template('analytics.html', posts=posts)

@app.route('/analytics/<name_of_party>')
def analytics_party(name_of_party):
    posts = Post.query.filter_by(name_of_party=name_of_party).all()
    my_plot_div = plot([Scatter(x=[post.upvote_counter for post in posts], y=[i+1 for i in range(len(posts))])], output_type='div')
    return render_template('graph_result.html', div_placeholder=Markup(my_plot_div))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__=="__main__":
    app.run()