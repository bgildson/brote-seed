# -*- coding: utf-8 -*-

from app.models import db


class PessoaModel(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    nome = db.Column(db.VARCHAR(80))

    def save(self):
        db.session.add(self)
        db.session.commit()
