# -*- coding: utf-8 -*-

from permission import Permission, PermissionDeniedException

from app.models.auth import AuthPermissionModel
from .rules import DenyRule


# todas as permissoes do resource
permissions = [
    AuthPermissionModel('#MetasGetAll', 'Listar todas as metas'),
    AuthPermissionModel('#MetasAdd', 'Adicionar uma meta'),
    AuthPermissionModel('#MetasGetOne', 'Seleciona uma meta'),
    AuthPermissionModel('#MetasUpdate', 'Atualiza uma meta'),
    AuthPermissionModel('#MetasRemove', 'Remove uma meta')
]

class TestPermission(Permission):
    def rule(self):
        return DenyRule()
