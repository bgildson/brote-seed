# -*- coding: utf-8 -*-

import os

from flask.cli import FlaskGroup

from app import create_app


cli = FlaskGroup(create_app=create_app)

@cli.command('populate-permissions', help='Criar as permissões iniciais')
def populate_auth_permissions():
    from app.models import db
    from app.models.auth import AuthPermissionModel

    tag_get_all = AuthPermissionModel()
    tag_get_all.tag = '#MetasGetAll'
    tag_get_all.description = 'Listar todas as metas'
    db.session.add(tag_get_all)

    tag_add = AuthPermissionModel()
    tag_add.tag = '#MetasAdd'
    tag_add.description = 'Adicionar uma meta'
    db.session.add(tag_add)

    tag_get_one = AuthPermissionModel()
    tag_get_one.tag = '#MetasGetOne'
    tag_get_one.description = 'Seleciona uma meta'
    db.session.add(tag_get_one)

    tag_update = AuthPermissionModel()
    tag_update.tag = '#MetasUpdate'
    tag_update.description = 'Atualiza uma meta'
    db.session.add(tag_update)

    tag_remove = AuthPermissionModel()
    tag_remove.tag = '#MetasRemove'
    tag_remove.description = 'Remove uma meta'
    db.session.add(tag_remove)

    db.session.commit()

@cli.command
def populate_auth_usuario_tag():
    from app.models import db
    from app.models.auth import AuthUsuarioTagModel

    auth_usuario_tag = AuthUsuarioTagModel()
    auth_usuario_tag.usuario_id = 1
    auth_usuario_tag.auth_tag_id = 1
    db.session.add(auth_usuario_tag)

    auth_usuario_tag = AuthUsuarioTagModel()
    auth_usuario_tag.usuario_id = 1
    auth_usuario_tag.auth_tag_id = 2
    db.session.add(auth_usuario_tag)

    auth_usuario_tag = AuthUsuarioTagModel()
    auth_usuario_tag.usuario_id = 1
    auth_usuario_tag.auth_tag_id = 3
    db.session.add(auth_usuario_tag)

    auth_usuario_tag = AuthUsuarioTagModel()
    auth_usuario_tag.usuario_id = 1
    auth_usuario_tag.auth_tag_id = 4
    db.session.add(auth_usuario_tag)
    db.session.commit()


if __name__ == '__main__':
    cli()
