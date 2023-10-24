from flask import Blueprint

componentsAPI = Blueprint('componentsAPI', __name__)

from . import ComponentsAPI
