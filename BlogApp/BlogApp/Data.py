from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime

from Models import Post
from InitDB import init_database

class Data:
    def __init__(self, engine):
        if not engine:
            raise ValueError('No Engine Found!')
        self.engine = engine
        db_engine = create_engine(engine)
        db_session = sessionmaker(bind=db_engine)
        self.session = db_session()

    def init_database(self):
        init_database(self.engine)

    def add_post(self, title, content, name_of_party, image, upvote_counter, downvote_counter, timestamp, video, location):
        new_post = Post(title=title, content=content, image=image, upvote_counter=upvote_counter, downvote_counter=downvote_counter, timestamp=timestamp, video=video, location=location)
        self.session.add(new_candidate)
        self.session.commit()
        return new_candidate.id

    def get_post(self, name_of_party=None, location=None, serialize_by_time=False, serialize_by_upvotes=False, show=False):
        all_posts = []
        if name_of_party is not None:
            all_posts = self.session.query(Post).filter(Post.name_of_party==name_of_party).all()
        elif location is not None:
            all_posts = self.session.query(Post).filter(Post.location==location).all()
        elif serialize_by_time:
            all_posts = self.session.query(Post).order_by(Post.timestamp).all()
        elif serialize_by_upvotes:
            all_posts = self.session.query(Post).order_by(Post.upvote_counter).all()
        else:
            all_posts = self.session.query(Post).order_by(Post.unique_id).all()

        if show:
            return [posts.returnObject() for posts in all_posts]
        else:
            return all_posts

    def delete_post(self, unique_id):
        if unique_id:
            items_deleted = self.session.query(Post).filter(Post.unique_id == unique_id).delete()
            return items_deleted > 0
        return False

    def fill_database(self):
        post1 = Post(title="New Elections", 
            content="Elections to be held in Gujrat", 
            name_of_party="BJP", 
            image="http://blogs.bu.edu/guidedhistory/bjp-logo-photos/", 
            upvote_counter=10, 
            downvote_counter=5, 
            timestamp=datetime.date(2017,9,10),
            video="AIzaSyAr78B7PUvpUqXlHsBAL8kEd3BRNOp6aEw,,,,,,",
            location="AIzaSyB1hPDbNRwBqg-msjWUq7anQOW4IynsP7M,,,"
        )
        self.session.add(post1)
        
            


