from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, text
from typing import Optional
from sqlalchemy import DateTime, Column, Integer, TIMESTAMP
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import deferred
from pydantic import BaseModel, validator
from src.utils import RedisClient
from sqlalchemy.ext.declarative import declared_attr
# Database ORM Configuration
redis = RedisClient()
db = SQLAlchemy(session_options={"expire_on_commit": False})


# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

# Database Migrations Configuration
migration = Migrate(db=db)

bcrypt = Bcrypt()


class DateTimeDbModelMixin(object):
    @declared_attr
    def created_at(cls):
        return deferred(
            Column(
                DateTime,
                default=text(
                    "CONVERT_TZ(NOW(), @@session.time_zone, '+00:00')")
            ),  group="dates"
        )

    @declared_attr
    def updated_at(cls):
        return deferred(
            Column(
                DateTime,
                default=text(
                    "CONVERT_TZ(NOW(), @@session.time_zone, '+00:00')"),
                onupdate=text(
                    "CONVERT_TZ(NOW(), @@session.time_zone, '+00:00')")
            ), group="dates"
        )


class IDDbModelMixin(object):

    @declared_attr
    def id(cls):
        return deferred(
            Column(Integer, primary_key=True, autoincrement=True, unique=True)
        )


class DbMixinModel(IDDbModelMixin, DateTimeDbModelMixin):
    ...
