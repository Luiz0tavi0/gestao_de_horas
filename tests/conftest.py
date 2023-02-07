from sqlalchemy.orm import undefer
import random
import re
from faker import Faker
from os.path import join
from json import dumps
# from dotenv import load_dotenv
from os import environ
import ipdb
from pytest import fixture
from src.utils import user as user_utils


@fixture(scope='module')
def app():
    from src.app import create_app
    # ipdb.set_trace()
    app = create_app()

    yield app


@fixture()
def client(app):
    return app.test_client()


@fixture()
def runner(app):
    return app.test_cli_runner()


@fixture(scope='function')
def random_user_already_registered(user_db):
    # ipdb.set_trace()
    users = user_db.query.options(undefer("id")).limit(10).all()
    user_already_registered = random.choice(users)
    return user_already_registered


@fixture(scope='function')
def user_db():
    from src.adapters.user import User
    return User


@fixture(scope='function')
def contract_db():
    from src.adapters.contract import Contract
    return Contract


@fixture(scope='function')
def task_db():
    from src.adapters.task import Task
    return Task


@fixture(scope='function')
def user_repo():
    from src.repository.user import UserRepository
    return UserRepository()


@fixture(scope='function')
def unauthenticated_headers():
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    return headers


@fixture
def header_with_access_token(random_user_already_registered):
    # ipdb.set_trace()

    # random_user_already_registered

    login_response = user_utils.make_login_response(
        random_user_already_registered)
    return {
        'Authorization': f'Bearer {login_response["token"]}',
        'Content-Type': 'application/json'
    }


@fixture(scope='function')
def fake_user():

    fake_factory = Faker('pt_br')
    payload = dumps(
        {
            "cpf": re.sub(r'\D', '', fake_factory.cpf()),
            "name": fake_factory.name(),
            "password": fake_factory.password(67),
            "email": fake_factory.email(),
            # "active": fake_factory.boolean(),
            "fone": re.sub(r'\D', '', fake_factory.phone_number()),
            "cnpj": re.sub(r'\D', '', fake_factory.cnpj()),
            "occupation": fake_factory.job(),
            # 'projects': []
        }
    )

    return payload


@fixture
def redis_client():
    from src.app import redis
    return redis
