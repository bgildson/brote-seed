# -*- coding: utf-8 -*-

from permission import Permission

from .rules import EndpointByTagRule


class EndpointByTagPermission(Permission):

    def __init__(self, tag):
        # classe mae chama no init o metodo "rule" que por sua vez utiliza o atributo "tag"
        self.tag = tag
        super().__init__()

    def rule(self):
        return EndpointByTagRule(self.tag)
