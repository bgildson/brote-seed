# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# registra models da aplicacao
from . import auth
from . import meta
from . import pessoa
from . import revoked_token
from . import usuario
