import ipdb
from typing import Optional
import os
import logging
from flask import Flask, jsonify
from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import init, stamp, migrate, upgrade
import src.utils.messages as msg
from src.config import settings
from src.adapters.user import User
from src.adapters import db, migration, bcrypt, redis
# from flask_apscheduler import APScheduler

# scheduler = APScheduler()

# interval examples
# @scheduler.task("interval", id="do_job_1", seconds=30, misfire_grace_time=900)
# def job1():
# """Sample job 1."""
# print(f"Job 1 executed -> {datetime.now()}")
# print(True if os.environ.get('ENV_SCHEDULER') == 'TRUE' else False)


# import ipdb;ipdb.set_trace()

# import sys; sys.path.append(os.path.pardir)

# Logs Initialization
console = logging.getLogger('console')

cors = CORS()


def config_db(app: Flask):
    # Database ORM Initialization

    db.init_app(app)
    bcrypt.init_app(app)
    app.db = db

# Database Migrations Initialization


def configure_migration(app: Flask):
    migration.init_app(app=app, db=app.db)


def configure_cors(app: Flask):
    cors.init_app(app)


jwt = JWTManager()


def configure_redis(app: Flask):
    redis.init_app(app)


def configure_jwt(app: Flask):
    from src.repository.user import UserRepository
    # Add jwt handler
    jwt.init_app(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(user_id):

        user = User.query.get(user_id)

        # Extender as informações do usuaŕio adicionando
        # novos campos: active, roles, full_name e etc...

        if user:
            return {'email': user.email, 'is_active': user.is_active, 'is_admin': user.is_admin}

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        return redis.token_exists(jti)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(
            status=401,
            message=msg.MSG_TOKEN_EXPIRED.format(
                datetime.utcfromtimestamp(jwt_payload.get('iat')))
        ), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(e):
        resp = jsonify({
            'status': 401,
            'description': e,
            'message': msg.MSG_PERMISSION_DENIED
        })

        resp.status_code = 401

        return resp


def config_routes(app: Flask):
    # import ipdb;ipdb.set_trace()
    from src.controllers import user_bp
    app.register_blueprint(user_bp)


def create_app(name=None):
    # Flask App Initialization
    app = Flask(__name__ if name is None else name)

    app.config.from_object(
        settings[os.environ.get('APPLICATION_ENV', 'default')])

#    import ipdb;ipdb.set_trace()
    configure_redis(app)

    # Add Routes
    config_routes(app)

    config_db(app)
    # import ipdb; ipdb.set_trace()
    # config_ma(app)
    configure_migration(app)

    configure_jwt(app)
    configure_cors(app)
    # import ipdb; ipdb.set_trace()
    check_and_upgrade_all_tables(app)  # , app.config['BASE_DIR'])
#   scheduler.init_app(app)
    # import ipdb; ipdb.set_trace()
    # scheduler.start()
    # import ipdb; ipdb.set_trace()
    return app


def check_and_upgrade_all_tables(app, directory=None):
    app.app_context().push()

    from src.adapters.user import User
    from src.adapters.contract import Contract
    from src.adapters.project import Project
    from src.adapters.task import Task
    # create database and tables
    # ipdb.set_trace()
    app.db.create_all()
    # import ipdb; ipdb.set_trace()
    if directory is None:
        directory = os.path.join(
            app.root_path, app.extensions['migrate'].directory)
    # checa se o diretório migrations já foi inicializado
    if not (os.access(directory, os.F_OK) and os.listdir(directory)):
        init(directory=directory)
    # ipdb.set_trace()
    stamp(directory=directory)
    migrate(directory=directory)
    upgrade(directory=directory)
