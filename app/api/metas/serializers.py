# -*- coding: utf-8 -*-

from flask_restplus import fields
from marshmallow import fields as f, Schema

from app.api import api


class MetaSchema(Schema):
    id = f.Int()
    descricao = f.Str()
    tipo = f.Int()


schema = MetaSchema()

model = api.model('meta', {
    'id': fields.Integer,
    'descricao': fields.String,
    'tipo': fields.Integer
})
