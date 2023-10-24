from . import defaultAPI
from flask import  jsonify, render_template, request, session, redirect, url_for
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
    if 'IsUserLoggedIn' not in session:
        session['IsUserLoggedIn'] = False

    if session['IsUserLoggedIn']:
        return render_template('menu.html', IsUserLoggedIn=session['IsUserLoggedIn'], UserType=session['UserType'])

    return render_template('index.html', IsUserLoggedIn=session['IsUserLoggedIn'], UserType=session.get('UserType', None))

@defaultAPI.route('/view_session')
def view_session():
    session_data = dict(session)
    return jsonify(session_data)

@defaultAPI.route('/page/<page>')
def page(page):
    if 'IsUserLoggedIn' not in session:
        session['IsUserLoggedIn'] = False

    if not session['IsUserLoggedIn'] and page not in ['login', 'signup']:
        return redirect(url_for('defaultAPI.index'))
    if session['IsUserLoggedIn'] and page in ['login', 'signup']:
        return redirect(url_for('defaultAPI.index'))
    
    return render_template(page + '.html', IsUserLoggedIn=session['IsUserLoggedIn'], UserType=session.get('UserType', None))