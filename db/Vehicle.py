from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    province_id = Column(Integer)
    city_id = Column(Integer)
    manufacturer_id = Column(String)
    terminal_model = Column(String)
    terminal_id = Column(String)
    license_plate_color = Column(Integer)
    plate_number = Column(String)

class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    warning_mark = Column(String)
    status_flag = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    altitude = Column(String)
    velocity = Column(String)
    plate_number = Column(String)
    direction = Column(Integer)
    time = Column(String)
