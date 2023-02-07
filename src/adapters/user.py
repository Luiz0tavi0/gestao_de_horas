from datetime import datetime
from os import getenv
from time import time
from typing import Optional, List
import jwt
from sqlalchemy_utils import EmailType

from pydantic import BaseModel, ValidationError, validator

from sqlalchemy.sql import expression
from sqlalchemy import Column, String, Integer, Numeric, Date, ForeignKey, DateTime, Boolean, func, event, Enum
from sqlalchemy.orm import relationship, deferred

from . import db, bcrypt, DateTimeDbModelMixin


class User(DateTimeDbModelMixin, db.Model):
    """ This is a base user Model """
    id = deferred(Column(db.Integer, primary_key=True,
                  autoincrement=True, unique=True))
    __tablename__ = 'users'
    # __mapper_args__ = {"concrete": True,}
    __mapper_args__ = {
        "polymorphic_identity": "users",
    }

    cpf = Column(String(11), primary_key=False, nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    email_confirmed_at = deferred(
        Column(DateTime, default=None, nullable=True))
    password = deferred(Column(String(350), nullable=False))
    email = Column(EmailType(), nullable=False, unique=True)
    fone = Column(String(15), default=None, nullable=True)
    active = Column(Boolean, default=expression.true(), nullable=False)
    cnpj = Column(String(14), default=None, nullable=True)
    occupation = Column(String(45), default=None, nullable=True)

    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    # time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    # relationship("Project", uselist=False, back_populates="user")

    # project: Mapper[Optional["Project"]] = relationship(back_populates="manager")
    projects = db.relationship('Project', backref='manager')

    def _gen_hash(self):
        self.password = bcrypt.generate_password_hash(
            self.password
        ).decode('utf-8')

    def verify_password(self, pwd: str):

        return bcrypt.check_password_hash(self.password, pwd)

    def set_password(self, pwd: str):
        self.password = bcrypt.generate_password_hash(pwd).decode('utf-8')

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return bool(self.cnpj)

    def __repr__(self):
        return f"<User('name={self.name}', email='{self.email}')>"
