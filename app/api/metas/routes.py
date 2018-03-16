# -*- coding: utf-8 -*-

from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restplus import fields, Resource

from app.models import db
from app.models.meta import MetaModel
from app.utils import populate
from app.utils.permissions import EndpointByTagPermission
from .. import api
from .serializers import model, schema, MetaSchema

from app.models import db


@api.route('/v1/metas')
class MetasResource(Resource):

    @api.marshal_with(model, envelope=current_app.config['API_ENVELOPE'])
    @jwt_required
    @EndpointByTagPermission('#MetasGetAll')
    def get(self, id=None):
        metas = MetaModel.query.all()

        return metas, 200

    @api.marshal_with(model, envelope=current_app.config['API_ENVELOPE'])
    @jwt_required
    @EndpointByTagPermission('#MetasAdd')
    def post(self):
        try:
            args = schema.dump(request.form).data

            meta = MetaModel()
            populate(meta, args)
            meta.save()

            return meta, 201
        except Exception as e:
            db.session.rollback()
            return 'Error', 400


@api.route('/v1/metas/<string:id>')
class MetasResource(Resource):

    @api.marshal_with(model, envelope=current_app.config['API_ENVELOPE'])
    @jwt_required
    @EndpointByTagPermission('#MetasGetOne')
    def get(self, id=None):
        meta = MetaModel.query.filter_by(id=id).first()

        if meta:
            return meta, 200
        else:
            return 'Meta não encontrada', 404

    @api.marshal_with(model, envelope=current_app.config['API_ENVELOPE'])
    @jwt_required
    @EndpointByTagPermission('#MetasUpdate')
    def put(self, id):
        try:
            args = schema.dump(request.form).data

            meta = MetaModel.query.filter_by(id=id).first()

            if not meta:
                return 'Meta não encontrada', 404

            populate(meta, args)

            db.session.update(meta)
            db.session.commit()

            return meta, 200
        except:
            db.session.rollback()
            return 'Error', 400

    @jwt_required
    @EndpointByTagPermission('#MetasRemove')
    def delete(self, id):
        try:

            meta = MetaModel.query.filter_by(id=id).first()

            if not meta:
                return 'Meta não encontrada', 404

            db.session.delete(meta)
            db.session.commit()

            return 'ok', 203
        except Exception as e:
            db.session.rollback()
            return 'Error'
