from flask import jsonify
from flask import abort
from flask import make_response
from flask import requests
from flask import url_for

from Data import Data
import datetime

db_engine = "sqlite:///foo.db'"

DATA_PROVIDER = Data(db_engine)

def post(name_of_party=None, location=None, serialize_by_time=False, serialize_by_upvotes=False, show=False):
    if name_of_party is not None:
        posts = DATA_PROVIDER.get_post(name_of_party=name_of_party, show=show)
    elif location is not None:
        posts = DATA_PROVIDER.get_post(location=location, show=show)
    elif serialize_by_time:
        posts = DATA_PROVIDER.get_post(serialize_by_time=serialize_by_time, show=show)   
    elif serialize_by_upvotes:
        posts = DATA_PROVIDER.get_post(serialize_by_upvotes=serialize_by_upvotes, show=show) 
    else:
       posts = DATA_PROVIDER.get_post(show=show)

    if show:
        return jsonify({
            "posts": posts,
            "total": len(posts)
        })
    else:
        return posts

def initialize_database():
    DATA_PROVIDER.init_database()

def fill_database():
    DATA_PROVIDER.fill_database()

def delete_post(unique_id):
    if DATA_PROVIDER.delete_post(unique_id):
        return make_response('', 204)
    else:
        return make_response('', 404)

def add_post():
    title = request.form["title"]
    content = request.form["content"]
    name_of_party = request.form["name_of_party"]
    image = request.form["image"]
    location = request.form["location"]
    video = request.form["video"]

    #get location!
    LOCATION_URL = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyB1hPDbNRwBqg-msjWUq7anQOW4IynsP7M"
    response = requests.post(url)
    response = response.json()
    latitude = str(response['location']['latitute'])
    longitude = str(response['location']['longitude'])
    accuracy = str(str(response['accuracy'])
    location = latitude + longitude + accuracy

    #get video!
    _VIDEO_API_KEY = "AIzaSyAr78B7PUvpUqXlHsBAL8kEd3BRNOp6aEw"

    new_post_id = DATA_PROVIDER.add_post(
        title=title,
        content=content,
        name_of_party=name_of_party,
        image=image,
        upvote_counter=0,
        downvote_counter=0,
        timestamp = datetime.datetime.now()
        location=location,
        # video=video
    )

    return jsonify({
        "id": new_post_id,
        "url": url_for("post_by_id", id=new_post_id)
    })