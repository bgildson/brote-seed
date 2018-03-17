# -*- coding: utf-8 -*-

from werkzeug.datastructures import Headers
from flask import (
    current_app, jsonify, request,
    Blueprint, Response
)
from flask_jwt_extended import (
    create_access_token, create_refresh_token, current_user,
    get_csrf_token, jwt_refresh_token_required, jwt_required,
    set_refresh_cookies, set_access_cookies, unset_jwt_cookies,
    JWTManager
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
            # cria tokens
            access_token = create_access_token(usuario)
            refresh_token = create_refresh_token(usuario)
            # resposta com csrf's
            res = jsonify({
                'access_csrf': get_csrf_token(access_token),
                'refresh_csrf': get_csrf_token(refresh_token)
            })
            # Set the JWT cookies in the response
            set_access_cookies(res, access_token)
            set_refresh_cookies(res, refresh_token)
            return res
        else:
            return jsonify({'login': False}), 401


@auth.route('/fresh-login')
class FreshLoginResource(Resource):

    def post(self):
        args = login_schema.dump(request.form)

        usuario = UsuarioModel.autenticate(args['usuario'], args['senha'])

        if usuario:
            access_token = create_access_token(usuario, fresh=True)
            res = jsonify({
                'access_csrf': get_csrf_token(access_token)
            })
            set_access_cookies(res, access_token)
            return res
        else:
            return { 'error': 'Usuário ou Senha incorreto' }, 400


@auth.route('/logout')
class LogoutResource(Resource):

    @jwt_required
    def post(self):
        res = jsonify({'logout': True})
        unset_jwt_cookies(res)
        return res


@auth.route('/refresh')
class RefreshResource(Resource):

    @jwt_refresh_token_required
    def post(self):
        access_token = create_access_token(current_user)
        res = jsonify({
            'access_csrf': get_csrf_token(access_token)
        })
        set_access_cookies(res, access_token)
        return res


# encapsula registro do modulo
def init_app(app):
    app.register_blueprint(auth_bp)
