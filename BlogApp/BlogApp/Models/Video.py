from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from Model import Model

class Video(Model): 
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