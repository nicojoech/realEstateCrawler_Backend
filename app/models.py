from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    crawler_agents = relationship("CrawlerAgent", back_populates="user")


class CrawlerAgent(Base):
    __tablename__ = 'crawler_agents'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    min_area = Column(String)
    max_price = Column(String)
    number_of_rooms = Column(Integer)
    zip_code = Column(String)
    state = Column(String)
    inUse = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="crawler_agents")
