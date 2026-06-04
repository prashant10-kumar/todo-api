from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, nullable = False)
    completed = Column(Boolean, default = False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    owner = relationship("User", back_populates = "todos")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    todos = relationship("Todo", back_populates = "owner")