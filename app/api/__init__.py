# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restplus import Api
from jwt import ExpiredSignatureError
from permission import PermissionDeniedException


# cria blueprint para API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# define qual a regra para acesso da api
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(api_bp, authorizations=authorizations, security=['apikey'])

'''
TODO: adicionar atributo 'action' para retorno dos errorhandler
para a aplicacao que esta consumindo a api qual acao pode ser tomada
para resolucao do erro
TODO: criar mapa de acoes possiveis
'''

# nao tem um usuario logado
@api.errorhandler(NoAuthorizationError)
def api_authorization_error_handler(error):
    return { 'message': 'você não está autorizado para acessar este recurso' }, 401

# usuario logado nao tem permissao para usar o recurso
@api.errorhandler(PermissionDeniedException)
def api_permission_error_handler(error):
    return { 'message': error.args[0] }, 401

# sessao do usuario expirou
@api.errorhandler(ExpiredSignatureError)
def api_expired_session_error_handler(error):
    return { 'message': 'sessão expirada' }, 401

# captura excecoes genericas
@api.errorhandler
def api_error_handler(error):
    # TODO: adicionar log para erros que entram neste handler
    return { 'message': error.args[0] }, 500

# registra apis
from . import metas
