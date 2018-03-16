# -*- coding: utf-8 -*-

import os

from flask import Flask
from flask_migrate import Migrate

from config import config


def create_app(script_info=None):
    app = Flask(__name__, instance_relative_config=True)

    # carrega a configuracao baseado no variavel de ambiente FLASK_CONFIG
    # ou utiliza a configuracao para um ambiente de desenvolvimento
    config_name = os.environ.get('FLASK_CONFIG', 'development')

    # configuracoes padroes baseadas no ambiente
    app.config.from_object(config[config_name])
    # configuracoes especificas locais
    app.config.from_pyfile('config.py')

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
        from app.api import api_bp
        from app.auth import auth_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(api_bp)

    return app
