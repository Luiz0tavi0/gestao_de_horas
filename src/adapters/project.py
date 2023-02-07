from datetime import datetime
from typing import Optional, List
from sqlalchemy.sql import expression
from sqlalchemy import Column, String, Integer, Numeric, Date, ForeignKey, DateTime, Boolean, func, event, Enum
from sqlalchemy.orm import relationship
from . import db, bcrypt, DbMixinModel
# from src.adapters.task import Task

class Project(db.Model, DbMixinModel):
    __tablename__ = 'projects'    
    __mapper_args__ = {"concrete": True,}

    # id = Column(Integer, primary_key=True, autoincrement=True, unique=True)

    name = Column(String(100), nullable=False, unique=True)
    start = Column(DateTime(), nullable=False, unique=False)
    end = Column(DateTime(), nullable=False, unique=False)
    status = Column(Enum('in_progress', 'stopped', 'done', name='status'),index=True)
    
   
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=False)
    # user_id = Column(ForeignKey('users.id'), primary_key=False)
    # user = relationship("User", back_populates="projects")
    
    # tasks = relationship("Contract", back_populates="project")