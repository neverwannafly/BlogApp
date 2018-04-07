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