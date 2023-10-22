from flask import Blueprint

defaultAPI = Blueprint('defaultAPI', __name__)

from . import HomeAPI
