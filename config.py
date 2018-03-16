# -*- coding: utf-8 -*-

from os import path


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.abspath('.'), 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_ENVELOPE = 'data'
    # headers(access token)
    # cookies(refresh token, apenas na rota de atualizacao)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_REFRESH_COOKIE_PATH = '/refresh'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class ConfigTest(Config):
    DEBUG = False


class ConfigDevelopment(Config):
    DEBUG = False


class ConfigProduction(Config):
    pass


config = {
    'test': ConfigTest,
    'development': ConfigDevelopment,
    'production': ConfigProduction
}
