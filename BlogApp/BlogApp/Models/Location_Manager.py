from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from Model import Model

class Location_Manager(Model):
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