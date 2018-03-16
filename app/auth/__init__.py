# -*- coding: utf-8 -*-

from werkzeug.datastructures import Headers
from flask import (
    current_app, jsonify, request,
    Blueprint, Response
)
from flask_jwt_extended import (
    create_access_token, create_refresh_token, current_user,
    jwt_refresh_token_required, jwt_required, JWTManager
)
from flask_restplus import Api, Resource
from marshmallow import fields, Schema

from app.models.usuario import UsuarioModel
from app.models.revoked_token import RevokedTokenModel


jwt = JWTManager()

auth_bp = Blueprint('auth', __name__)

# configura autenticacao
# baseado no nome do usuario
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return usuario.usuario

# obtem o objeto do atual usuario
@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return UsuarioModel.query.filter_by(usuario=identity).first()

# trata mensagem de erro no acesso a um endpoint nao acessivel
@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "message": "User {} not found".format(identity)
    }
    return jsonify(ret), 401

# verifica se o access/refresh token esta na blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)


auth = Api(auth_bp)


class LoginSchema(Schema):
    usuario = fields.Str(required=True, min_length=6)
    senha = fields.Str(required=True)


login_schema = LoginSchema()


@auth.route('/login')
class LoginResource(Resource):

    def post(self):
        args = login_schema.dump(request.form).data

        usuario = UsuarioModel.autenticate(args['usuario'], args['senha'])

        if usuario:
            res = jsonify({'access_token': create_access_token(usuario) })
            res.set_cookie(
                current_app.config['JWT_REFRESH_COOKIE_NAME'],
                create_refresh_token(usuario),
                path=current_app.config['JWT_REFRESH_COOKIE_PATH']
            )
            return res
            # return {
            #     'access_token': create_access_token(usuario),
            #     'refresh_token': create_refresh_token(usuario)
            # }, 200, headers
        else:
            return { 'error': 'Usuário ou Senha incorreto' }, 400


@auth.route('/fresh-login')
class FreshLoginResource(Resource):

    def post(self):
        args = login_schema.dump(request.form)

        usuario = UsuarioModel.autenticate(args['usuario'], args['senha'])

        if usuario:
            return {
                'access_token': create_access_token(usuario, fresh=True)
            }, 200
        else:
            return { 'error': 'Usuário ou Senha incorreto' }, 400


# @auth.route('/logout')
# class LogoutResource(Resource):

#     @jwt_required
#     def post(self):
#         args = login_parser.parse_args()

#         usuario = UsuarioModel.autenticate(args['usuario'], args['senha'])

#         if usuario:
#             return {}, 200
#         else:
#             return { 'error': 'Usuário ou Senha incorreto' }, 400


@auth.route('/refresh')
class RefreshResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        return { 'access_token': create_access_token(identity=current_user) }, 200
