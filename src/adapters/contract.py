from datetime import datetime
from sqlalchemy.sql import expression
from sqlalchemy import Column, String, Integer, Numeric, Date, ForeignKey, DateTime, Boolean, func, event, Enum
from sqlalchemy.orm import relationship

from . import db , DateTimeDbModelMixin

class Contract(db.Model, DateTimeDbModelMixin):
    __tablename__ = 'contracts'
    __mapper_args__ = {"concrete": True,}
    
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)

    description = Column(String(450), nullable=True, unique=True)
    active = Column(Boolean, default=expression.true(), nullable=False)


    # user_id = Column(ForeignKey('users.id'), primary_key=False)
    # user = relationship("User", back_populates="projects")

    # project_id = Column(ForeignKey('projects.id'), primary_key=False)    
    # project = relationship("Project", back_populates="tasks")