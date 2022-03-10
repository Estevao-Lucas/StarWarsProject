from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    favorite_char = relationship("Character", back_populates="owner")

class Character(Base):
    __tablename__ = "character"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    height = Column(String, index=True)
    mass = Column(String, index=True)
    hair_color = Column(String, index=True)
    skin_color = Column(String, index=True)
    eye_color = Column(String, index=True)
    birth_year = Column(String, index=True)
    gender = Column(String, index=True)
    owner_id = Column(ForeignKey("users.id"))

    owner = relationship("User", back_populates="favorite_char")

