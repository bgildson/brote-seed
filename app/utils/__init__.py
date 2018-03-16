# -*- coding: utf-8 -*-

def populate(model, data):
    for key, value in data.items():
        setattr(model, key, value)
