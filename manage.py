# -*- coding: utf-8 -*-

import os

from flask.cli import FlaskGroup

from app import create_app


cli = FlaskGroup(create_app=create_app)

@cli.command('populate-permissions', help='Criar as permissões iniciais')
def populate_auth_permissions():
    from app.models import db
    from app.models.auth import AuthPermissionModel

    tag_get_all = AuthPermissionModel('#MetasGetAll', 'Listar todas as metas')
    db.session.add(tag_get_all)

    tag_add = AuthPermissionModel('#MetasAdd', 'Adicionar uma meta')
    db.session.add(tag_add)

    tag_get_one = AuthPermissionModel('#MetasGetOne', 'Seleciona uma meta')
    db.session.add(tag_get_one)

    tag_update = AuthPermissionModel('#MetasUpdate', 'Atualiza uma meta')
    db.session.add(tag_update)

    tag_remove = AuthPermissionModel('#MetasRemove', 'Remove uma meta')
    db.session.add(tag_remove)

    db.session.commit()

@cli.command
def populate_auth_usuario_permissions():
    from app.models import db
    from app.models.auth import AuthUsuarioPermissionModel

    auth_usuario_tag = AuthUsuarioPermissionModel(1, 1)
    db.session.add(auth_usuario_tag)

    auth_usuario_tag = AuthUsuarioPermissionModel(1, 2)
    db.session.add(auth_usuario_tag)

    auth_usuario_tag = AuthUsuarioPermissionModel(1, 3)
    db.session.add(auth_usuario_tag)

    auth_usuario_tag = AuthUsuarioPermissionModel(1, 4)
    db.session.add(auth_usuario_tag)

    db.session.commit()

if __name__ == '__main__':
    cli()
