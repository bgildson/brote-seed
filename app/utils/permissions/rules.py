# -*- coding: utf-8 -*-

from flask_jwt_extended import current_user
from permission import Rule, PermissionDeniedException


class EndpointByTagRule(Rule):

    def __init__(self, tag):
        super().__init__()
        self.tag = tag
        # tenta pegar uma descricao para a tag ou,
        # se n encontrar uma, utiliza a padrao
        self.error_description = 'você não tem permissão para acessar este recurso'

    def check(self):
        return current_user.has_permission(self.tag)

    def deny(self):
        raise PermissionDeniedException(self.error_description)
