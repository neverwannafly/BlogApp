# Defines the models that are to be used in the project!

# Imports
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from Model import Model

# Defines the Post model which would be displayed on the website!
class Post(Model):
    # Class attributes
    __tablename__ = "post"
    unique_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(100), default="NO_TITLE")
    content = Column(String(1000, default=""))
    upvote_counter = Column(Integer)
    downvote_counter = Column(Integer)
    time_stamp = Column(Date)
    location = relationship("Location_Manager")
    video = relationship("Video")

    # Methods
    def returnObject(self):
        return {
            "unique_id" : self.unique_id,
            "title" : self.title,
            "content" : self.content,
            "upvote_counter" : self.upvote_counter,
            "downvote_counter" : self.downvote_counter,
            "time_stamp" : self.time_stamp,
            # Add Location and Video to this too!
        }

class Location_Manager:
    # Class attributes
    _API_KEY = "AIzaSyB1hPDbNRwBqg-msjWUq7anQOW4IynsP7M"
    __tablename__ = "location_manager"
    unique_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    latitude = Column(Integer)
    longitude = Column(Integer)
    accuracy = Column(Integer)
    # Methods
    def returnObject(self):
        return {
            "unique_id" : self.unique_id,
            "latitude" : self.latitude,
            "longitude" : self.longitude,
            "accuracy" : self.accuracy,
        }

class Video: 
    # Class attributes
    _API_KEY = "AIzaSyAr78B7PUvpUqXlHsBAL8kEd3BRNOp6aEw"
    __tablename__ = "video"
    unique_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    view_count = Column(String)
    like_count = Column(String)
    dislike_count = Column(String)
    favourite_count = Column(String)
    comment_count = Column(String)
    url = Column(String)

    # Methods
    def returnObject(self):
        return {
            "unique_id" : self.unique_id,
            "view_count" : self.view_count,
            "like_count" : self.like_count,
            "dislike_count" : self.dislike_count,
            "favourite_count" : self.favourite_count,
            "comment_count" : self.comment_count,
            "url" : self.url
        }
