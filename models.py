from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase

# Models
class Base(DeclarativeBase):
    pass

class SensorData(Base):
    __tablename__ = "sensor_data"
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    metric = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime)
