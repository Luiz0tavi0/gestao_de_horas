import sys
from os import getenv
import jwt
from time import time
from typing import Type, Optional
import ipdb
from flask import current_app
from werkzeug.exceptions import NotFound
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError
from redis import StrictRedis
from src.service_layer.interfaces.user import IUserService
from src.repository.user import UserRepository
from src.repository.interfaces.user import IUserRepository
from src.serializer.user import *
from src.serializer.validate_errors import ErrorUserValidateSchema, ErrorUserIntegrity
from src.adapters import redis
from src.utils.user import make_login_response


class UserService(IUserService):
    def __init__(self, repo: Optional[Type[IUserRepository]] = None):

        self._repo = UserRepository if repo is None else repo

    def signin(self, data):
        currentFuncName = sys._getframe().f_code.co_name
        try:
            #
            valid_schema = UserSignin(**data)
        except ValidationError as v_err:
            list_errors = v_err.errors()

            def f(x): return x.get('ctx', {'status_error': None}) != None
#
            try:
                status_code = list(filter(f, list_errors))[
                    0]['ctx']['status_error']
            except KeyError:
                status_code = 422
            instance = f"{self.__class__.__name__}/{currentFuncName}"
            items_errors = {'title': 'Validate Error', 'instance': instance, 'errors': list_errors,
                            'status_code': status_code}
            resp_err = ErrorUserValidateSchema(**items_errors)
            return resp_err.dict(by_alias=False)
        else:
            try:
                user = self._repo().create(valid_schema)

            except IntegrityError as db_error:

                items_errors = {
                    'title': db_error.__class__.__name__,
                    'instance': f"{self.__class__.__name__}/{currentFuncName}",
                    'error': db_error.orig.msg,
                    'status_code': 422
                }
                return ErrorUserIntegrity(**items_errors).dict(by_alias=False)

        return UserSigninSuccess.from_orm(user).dict()

    def update(self, current_user: int, data) -> dict:
        currentFuncName = sys._getframe().f_code.co_name

        try:
            #
            valid_schema = UserUpdateSchema(**data)
#
            user_data = valid_schema.dict(
                exclude_unset=True, exclude_defaults=True)
        except ValidationError as v_err:
            list_errors = v_err.errors()
            def f(x): return x.get('ctx', {'status_error': None}) != None
            try:
                status_code = list(filter(f, list_errors))[
                    0]['ctx']['status_error']
            except KeyError:
                status_code = 422
            instance = f"{self.__class__.__name__}/{currentFuncName}"
            items_errors = {'title': 'Validate Error', 'instance': instance,
                            'errors': list_errors, 'status_code': status_code}
            resp_err = ErrorUserValidateSchema(**items_errors)
            return resp_err.dict(by_alias=False)
        else:
            #
            try:
                result = self._repo().update(current_user, user_data)

            except IntegrityError as db_error:
                items_errors = {
                    'title': db_error.__class__.__name__,
                    'instance': f"{self.__class__.__name__}/{currentFuncName}",
                    'error': db_error.orig.msg,
                    'status_code': 400
                }
                return ErrorUserIntegrity(**items_errors).dict(by_alias=False)
            else:
                if result:
                    #
                    return UserUpdateSchemaSuccess(
                        msg="user updated successfully", status_code=204, status='Ok').dict()
                #
                return UserUpdateSchemaSuccess(msg="user not modified", status_code=304, status='Ok').dict()

    def change_password(self, user_id: int, data, jtw: dict):
        currentFuncName = sys._getframe().f_code.co_name
        try:
            ipdb.set_trace()
            valid_schema = UserCredentialsSchema(**data)

        except ValidationError as v_err:
            list_errors = v_err.errors()
            def f(x): return x.get('ctx', {'status_error': None}) != None
            try:
                status_code = list(filter(f, list_errors))[
                    0]['ctx']['status_error']
            except KeyError:
                status_code = 422
            instance = f"{self.__class__.__name__}/{currentFuncName}"
            items_errors = {'title': 'Validate Error', 'instance': instance,
                            'errors': list_errors, 'status_code': status_code}
            resp_err = ErrorUserValidateSchema(**items_errors)
            return resp_err.dict(by_alias=False)

        else:
            try:
                ipdb.set_trace()
                user = self._repo().change_password(user_id, valid_schema.password)
            except IntegrityError as db_error:
                items_errors = {
                    'title': db_error.__class__.__name__,
                    'instance': f"{self.__class__.__name__}/{currentFuncName}",
                    'error': db_error.orig.msg,
                    'status_code': 422
                }
                return ErrorUserIntegrity(**items_errors).dict(by_alias=False)
            else:
                ipdb.set_trace()
                self.logout(jtw)
                return UserUpdateCredentialsSuccess(status_code=302).dict()

    def login(self, data):
        currentFuncName = sys._getframe().f_code.co_name
        try:
            valid_schema = UserLogin(**data)
        except ValidationError as v_err:
            list_errors = v_err.errors()
            instance = f"{self.__class__.__name__}/{currentFuncName}"
            items_errors = {'title': "Invalid email or password",
                            'instance': instance, 'errors': list_errors, 'status_code': 422}
            resp_err = ErrorUserValidateSchema(**items_errors)
            return resp_err.dict(by_alias=False)

        else:
            try:
                user = self._repo().get_user_by_email(valid_schema.email.lower())

                if user.verify_password(valid_schema.password):
                    return UserLoginSuccess(**make_login_response(user)).dict()

                return UserLoginFail(
                    **{'title': 'Password or email incorrect.',
                       'errors': 'The email or password you entered is incorrect. Please try again or reset your password.',
                       'instance': f"{self.__class__.__name__}/{currentFuncName}",
                       'status_code': 401}
                ).dict()

            except NotFound as err:

                items_errors = {
                    'title': err.__class__.__name__,
                    'instance': f"{self.__class__.__name__}/{currentFuncName}",
                    'error': err.name,
                    'status_code': err.code
                }

                return ErrorUserIntegrity(**items_errors).dict(by_alias=False)

    def logout(self, jwt: dict):
        redis.include_jwt_in_blocklist(jwt)
        return redis.jwt_blocklist.exists(jwt['jti'])

    def get_reset_token(self, expires: int = 900, user_email: str = '') -> str | dict:
        currentFuncName = sys._getframe().f_code.co_name
        try:
            valid_schema = UserResetPassword(email=user_email)
        except ValidationError as v_err:
            list_errors = v_err.errors()
            instance = f"{self.__class__.__name__}/{currentFuncName}"
            items_errors = {'title': "Invalid email",
                            'instance': instance, 'errors': list_errors, 'status_code': 422}
            resp_err = ErrorUserValidateSchema(**items_errors)
            return resp_err.dict(by_alias=False)

        ipdb.set_trace()
        user = self._repo().get_user_by_email(valid_schema.email)

        return {
            'reset_token': jwt.encode({'reset_password': user.name, 'user_id': user.id, 'exp': time() + expires}, key=getenv('SECRET_KEY'))
        }

    def verify_reset_token(self, token):
        try:
            username = jwt.decode(token, key=getenv(
                'SECRET_KEY_FLASK'))['reset_password']
            print(username)
        except Exception as e:
            print(e)
            return
        return User.query.filter_by(username=username).first()
