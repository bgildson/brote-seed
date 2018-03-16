# -*- coding: utf-8 -*-

from . import db


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_token'

    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    jti = db.Column(db.String)

    @classmethod
    def is_jti_blacklisted(cls, jti):
        return bool(cls.query.filter_by(jti=jti).first())
