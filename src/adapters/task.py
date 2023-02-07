from datetime import datetime
from sqlalchemy.sql import expression
from sqlalchemy import Column, String, Integer, Numeric, Date, ForeignKey, DateTime, Boolean, func, event, Enum
from sqlalchemy.orm import relationship
from src.adapters.project import Project
from . import db, bcrypt, DateTimeDbModelMixin


class Task(DateTimeDbModelMixin, db.Model):
    __tablename__ = 'tasks'
    __mapper_args__ = {"concrete": True,}
    
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(450), nullable=False, unique=False)
    billable = Column(Boolean, server_default=expression.true(), nullable=False)
    description = Column(String(450), nullable=False, unique=False)
    status = Column(Enum('in_progress', 'stopped', 'done', name='status'), index=True)
    date = Column(DateTime, default=datetime.now, nullable=False)
    hours = Column(Integer(), nullable=False)
    billable = Column(Boolean, server_default=expression.true(), nullable=False)

    # user = relationship("User", back_populates="task")
    # user_id = Column(Integer, ForeignKey('users.id'))

    # project = relationship("Project", back_populates="task")
    # project_id = Column(Integer, ForeignKey('projects.id'))