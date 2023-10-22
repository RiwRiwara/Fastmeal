from . import defaultAPI
from flask import  jsonify, render_template, request
import json
from Backend.Constant import Constants
from Backend.db import db

@defaultAPI.route('/testapi', methods=['GET'])
def api_entry():
    response = {
        'data': "API Running"
    }
    return jsonify(response)

@defaultAPI.route('/get-collections', methods=['GET'])
def get_data_from_db():
    AllCollection = db.list_collection_names()
    response = {
        'Collections': AllCollection
    }
    return jsonify(response)

@defaultAPI.route('/')
def index():
    return render_template('index.html')

@defaultAPI.route('/page/<page>')
def page(page):
    return render_template(page)
