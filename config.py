# -*- coding: utf-8 -*-

import os


class BaseConfig:
    DEBUG = False
    TESTING = False

    # pasta root do projeto
    PROJECT_ROOT = os.path.abspath('.')

    # connection string para banco
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, 'db.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # envelope das responstas do api
    API_ENVELOPE = 'data'

    # gera chave aleatoria, se n estiver em producao
    JWT_SECRET_KEY = os.urandom(32)
    # utiliza csrf para combinar
    JWT_COOKIE_CSRF_PROTECT = True
    # cliente sera forçado a passar o csrf token nos headers da request
    JWT_CSRF_IN_COOKIES = False
    # sempre buscar os tokens nos cookies
    JWT_TOKEN_LOCATION = ['cookies']
    # tokens de acesso serão buscados desde o root
    JWT_ACCESS_COOKIE_PATH = '/'
    # so pergunta pelo refresh token qndo acessando caminho /refresh
    JWT_REFRESH_COOKIE_PATH = '/refresh'
    # habilita macanismo para revogar um token mesmo este ainda não estando vencido
    JWT_BLACKLIST_ENABLED = True
    # blacklist será aplicada para tokens de acesso e de refresh
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True

    # usar sqlite em memoria, qndo testando
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
