from flask import Blueprint

userAPI = Blueprint('userAPI', __name__)

from . import UserAPI
