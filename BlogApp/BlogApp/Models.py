from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
import enum

Model = declarative_base()

# Video (Layout) -> 
#     _API_KEY = "AIzaSyAr78B7PUvpUqXlHsBAL8kEd3BRNOp6aEw" -> 0
#     view_count = "" -> 1
#     like_count = "" -> 2
#     dislike_count = "" -> 3
#     favourite_count = "" -> 4
#     comment_count = "" -> 5
#     url = "" -> 6

# Location_Manager (Layout) ->
#     _API_KEY = "AIzaSyB1hPDbNRwBqg-msjWUq7anQOW4IynsP7M" -> 0
#     latitude = "" -> 1
#     longitude = "" -> 2
#     accuracy = "" -> 3


# Defines the Post model which would be displayed on the website!
class Post(Model):
    # Class attributes
    __tablename__ = "post"
    unique_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(100), default="NO_TITLE")
    content = Column(String(1000), default=" ")
    name_of_party = Column(String(100), default=" ")
    image = Column(String(200))
    upvote_counter = Column(Integer)
    downvote_counter = Column(Integer)
    timestamp = Column(Date)
    location = Column(String(500), default=",,")
    video = Column(String(500), default=",,,,,")
    
    # Methods
    def returnObject(self):
        location = location.split(',')
        video = video.split(',')
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
                "url" : self[5],
            }
        }