# -*- coding: utf-8 -*-

from app.models import db


class AuthPermissionModel(db.Model):
    __tablename__ = 'auth_permissions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(120))
    # description_error = db.Column(db.String(120))

    def __init__(self, tag, description='', *args, **kwargs):
        self.tag = tag
        self.description = description


class AuthUsuarioPermissionModel(db.Model):
    __tablename__ = 'auth_usuarios_permissions'

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    auth_tag_id = db.Column(db.Integer, db.ForeignKey('auth_permissions.id'), primary_key=True)

    auth_tag = db.relationship('AuthPermissionModel')
