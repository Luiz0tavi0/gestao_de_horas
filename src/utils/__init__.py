from functools import wraps
from typing import Optional
import ipdb
from flask import Flask
from flask_jwt_extended import get_jwt_identity, get_jwt, verify_jwt_in_request
from redis import StrictRedis
from src.utils.responses import resp_notallowed_user


class RedisClient(object):

    def __init__(self, app=None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask, **kwargs):
        self.jwt_blocklist = StrictRedis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'],
            decode_responses=True
        )
        self.ACCESS_EXPIRES = max(
            app.config['JWT_ACCESS_TOKEN_EXPIRES'], app.config['JWT_REFRESH_TOKEN_EXPIRES'])

    def include_jwt_in_blocklist(self, jwt: dict):  # token: str):
        # ipdb.set_trace()
        ACCESS_EXPIRES = int((jwt['exp']-self.jwt_blocklist.time()[0])*1.1)
        token = jwt["jti"]
        self.jwt_blocklist.set(token, "", ex=ACCESS_EXPIRES)

    def token_exists(self, token: str) -> bool:
        exists = self.jwt_blocklist.exists(token)
        return exists != 0


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return resp_notallowed_user()
        return decorator
    return wrapper


def owner_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_active"]:
                kwargs['user_id'] = get_jwt_identity()
                return fn(*args, **kwargs)
            else:
                return resp_notallowed_user()
        return decorator
    return wrapper
