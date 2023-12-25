""" DocDocDocDocDocDoc
"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.ratings import *
from api.v1.views.comments import *
from api.v1.views.likes import *
from api.v1.views.chats import *
from api.v1.views.items import *
