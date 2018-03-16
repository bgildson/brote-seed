# -*- coding: utf-8 -*-

from app.models import db


class MetaModel(db.Model):
    __tablename__ = 'metas'

    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    descricao = db.Column(db.VARCHAR(80))
    tipo = db.Column(db.INT)

    def save(self):
        db.session.add(self)
        db.session.commit()
