# -*- coding: utf-8 -*-

import hashlib

from sqlalchemy import and_

from app.models import db
from app.models.auth import AuthPermissionModel, AuthUsuarioPermissionModel


class UsuarioModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(15))
    senha = db.Column(db.String(64))
    pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoas.id'))
    admin = db.Column(db.Boolean)

    @classmethod
    def autenticate(cls, usuario, senha):
        return cls.query.filter_by(
            usuario=usuario,
            senha=hashlib.sha256(senha.encode('utf-8')).hexdigest()
        ).first()

    def has_permission(self, tag):
        return bool(
            self.is_admin or
            AuthUsuarioPermissionModel
                .query
                .filter(and_(
                    AuthUsuarioPermissionModel.usuario_id == self.id,
                    AuthPermissionModel.tag == tag
                ))
                .join((AuthPermissionModel,
                       AuthPermissionModel.id == AuthUsuarioPermissionModel.auth_tag_id))
                .first()
        )

    def set_senha(self, senha):
        self.senha = hashlib.sha256(senha.encode('utf-8')).hexdigest()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def is_admin(self):
        return self.admin
