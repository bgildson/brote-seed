# -*- coding: utf-8 -*-

from permission import PermissionDeniedException, Rule


class DenyRule(Rule):
    def check(self):
        return False

    def deny(self):
        raise PermissionDeniedException('você não tem essa permissão, ze gotinha', 405)
