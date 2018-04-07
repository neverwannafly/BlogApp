from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()

def init_database(engine):
    db_engine = create_engine(engine, echo=True)
    Model.metadata.create_all(db_engine)
