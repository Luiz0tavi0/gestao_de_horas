# -*- coding: utf-8 -*-
import os
from datetime import timedelta


class Config:

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    # PORT = int(os.environ.get('PORT', 5000))
    # DEBUG = os.environ.get('DEBUG') or False
    PROPAGATE_EXCEPTIONS = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', f"sqlite:///{LOCAL_DATABASE_URI}")

    # import ipdb;ipdb.set_trace()
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 7200)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 6)))

    # project root directory
    # os.path.join(os.pardir, os.path.dirname(__file__))
    BASE_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__), os.pardir))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # SECRET_KEY = os.environ.get("SECRET_KEY")

    # REDIS Configuration
    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    # Flask Configuration
    # --------------------------------------------------------------------
    DEBUG = os.environ.get('DEBUG') or False
    TESTING = False
    PORT = int(os.environ.get('PORT', 5000))

    # log file path
    # --------------------------------------------------------------------
    enable_access_log = False
    log_socket_host = "127.0.0.1"
    log_socket_port = 514

    # SCHEDULELER
    # --------------------------------------------------------------------
    # import ipdb; ipdb.set_trace()
    SCHEDULER_API_ENABLED = True if os.environ.get(
        'ENV_SCHEDULER') == 'TRUE' else False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ENGINE_OPTIONS = {

        'case_sensitive': False,
        'echo': True,
        'echo_pool': True
    }

    # SMTP server main
    # --------------------------------------------------------------------

    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
    EMAIL_HOST = os.environ.get('EMAIL_HOST')
    EMAIL_PORT = os.environ.get('EMAIL_PORT')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


class DevelopmentConfig(Config):

    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = True
    ASSETS_DEBUG = True


class TestingConfig(Config):

    ENV = os.environ.get("FLASK_ENV", "testing")
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):

    ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = False
    USE_RELOADER = False


settings = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
