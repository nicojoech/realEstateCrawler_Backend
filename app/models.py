from sqlalchemy import Column, Integer, String, Float, Boolean

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class CrawlerAgent(Base):
    __tablename__ = 'crawler_agents'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    min_area = Column(Float)
    max_price = Column(Float)
    number_of_rooms = Column(Integer)
    zip_code = Column(String)
    state = Column(String)
    rent = Column(Boolean)
    type = Column(String)
