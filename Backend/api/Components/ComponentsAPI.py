from . import componentsAPI
from flask import  jsonify, render_template, request
import json
from Backend.Constant import Constants
from Backend.db import db

@componentsAPI.route('/', methods=['GET'])
def api_entry():
    response = {
        'data': "ComponetsAPI Running"
    }
    return jsonify(response)
