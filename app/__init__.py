# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_migrate import Migrate


CONFIG_NAME_MAPPER = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
    'local': 'local_config.LocalConfig',
}

def create_app(script_info=None):
    app = Flask(__name__, instance_relative_config=True)

    # carrega a configuracao baseado no variavel de ambiente FLASK_CONFIG
    # ou utiliza a configuracao para um ambiente de desenvolvimento
    config_name = os.getenv('FLASK_CONFIG', 'development')

    # configuracoes padroes baseadas no ambiente
    app.config.from_object(CONFIG_NAME_MAPPER[config_name])

    with app.app_context():
        # registra database
        from app.models import db
        db.init_app(app)

        # inicia extensao de migrate
        migrate = Migrate()
        migrate.init_app(app=app, db=db)

        # registra modulo de autenticacao
        from app.auth import jwt
        jwt.init_app(app)

        # registra modulos de resources
        from app import auth
        auth.init_app(app)
        from app import api
        api.init_app(app)

    return app
