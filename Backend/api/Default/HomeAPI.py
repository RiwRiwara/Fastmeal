from . import defaultAPI
from flask import  jsonify, render_template, request, session, redirect, url_for, send_file
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
        return redirect(url_for('defaultAPI.page', page='menu'))

    return render_template('index.html', IsUserLoggedIn=session['IsUserLoggedIn'], UserType=session.get('UserType', None), pageData=None)

@defaultAPI.route('/static/images', methods=['GET'])
def serve_image():
    name = request.args.get('name')
    filename = f'Frontend\\static\\images/{name}' 

    return send_file(filename, mimetype='image/jpeg')

@defaultAPI.route('/view_session')
def view_session():
    session_data = dict(session)
    return jsonify(session_data)

@defaultAPI.route('/page/<page>')
def page(page):
    if 'IsUserLoggedIn' not in session:
        session['IsUserLoggedIn'] = False
    if 'UserType' not in session:
        session['UserType'] = "customer"


    if not session['IsUserLoggedIn'] and page not in ['login', 'signup']:
        return redirect(url_for('defaultAPI.index'))
    if session['IsUserLoggedIn'] and page in ['login', 'signup']:
        return redirect(url_for('defaultAPI.index'))
    if session['UserType'] == 'customer' and page in ['admin']:
        return redirect(url_for('defaultAPI.index'))
    return renderPage(page, request.args)

def renderPage(page, args):
    pageData = {}
    if page == 'menu':
        if 'cart_items' not in session:
            session['cart_items'] = {}
        filter_dict = {}
        if args.get('name', None):  
            name = args.get('name', None)  
            filter_dict['name'] = {'$regex': name, '$options': 'i'} 
        food_data = list(db.food_items.find(filter_dict, {'_id': 0}))

        pageData = {
            'title': 'Menu',
            'data': food_data,
            'isCart': False
        }
    elif page == 'login':
        pageData['title'] = 'Login'
    elif page == 'signup':
        pageData['title'] = 'Signup'
    elif page == 'cart':
        if 'cart_items' not in session or len(session['cart_items']) == 0:
            pageData = {
                'title': 'Menu',
            }
            return redirect(url_for('defaultAPI.page', page='menu'))
        data = []
        total = 0
        for i in session['cart_items']:
            item = db.food_items.find_one({"id": i})
            item['quantity'] = session['cart_items'][i]['quantity']
            item['total_price'] = float(item['price'].split()[0]) * int(session['cart_items'][i]['quantity'])
            data.append(item)
            total += float(item['price'].split()[0]) * int(session['cart_items'][i]['quantity'])
        pageData = {
            'title': 'Cart',
            'email': session.get('email', None),
            'data': data,
            'foodsID': json.dumps(list(session['cart_items'].keys())),
            'address': db.users.find_one({"email": session.get('email', None)})['address'],
            'total': total,
            'isCart': True,
        }
    elif page == 'orders':
        order_id = args.get('id', None)
        if order_id:
            pageData = {
                'order_id' : order_id,
                'title': 'Order Detail',
                'data': db.order_items.find_one({"id": order_id}),
                'isOrderDetail': True,
            }
        else:
            listOrder = db.order_items.find({"email": session.get('email', None)})
            pageData = {
                'title': 'Order',
                'data': listOrder,
                'isOrderDetail': False,
            }
    elif page == 'message':
            order_id = args.get('id', None)
            if order_id:
                pageData = {
                    'order_id' : order_id,
                    'title': 'Order Detail',
                    'data': db.order_items.find_one({"id": order_id}),
                    'isOrderDetail': True,
                }
            else:
                listOrder = db.order_items.find({})
                pageData = {
                    'title': 'Message',
                    'data': listOrder,
                    'isOrderDetail': False,
                }
    elif page == 'admin':
        listOrder = db.food_items.find({})
        pageData = {
                'title': 'Admin',
                'data': listOrder,
            }
        
    elif page == 'edit-profile':
        pageData['title'] = 'Edit Profile'
        pageData = {
            'title': 'Edit Profile',
            'data': db.users.find_one({"email": session.get('email', None)})
        }
    return render_template(page + '.html', IsUserLoggedIn=session['IsUserLoggedIn'], UserType=session.get('UserType', None), pageData=pageData)


@defaultAPI.route('/summary', methods=['GET'])
def get_summary():
    summary_data = {
        "collection_data": [],
        "summary": {}
    }

    collection_names = ['food_items', 'order_items', 'users']
    summaryAll = {
        "total": 0,
        "confirmed": 0,
        "cancelled": 0,
        "waiting": 0,
        "income": 0,
        }
    for collection_name in collection_names:
        collection = db[collection_name]

        summary = {
            'collection_name': collection_name,
            'document_count': collection.count_documents({}),
            'alldata': list(collection.find({}, {'_id': 0})),
        }

        if collection_name == 'order_items':
            for i in summary['alldata']:
                summaryAll['income'] += float(i['total'])

            summary['confirmed'] = collection.count_documents({"status": "confirmed"})
            summary['cancelled'] = collection.count_documents({"status": "cancel"})
            summary['waiting'] = collection.count_documents({"status": "waiting"})
            summaryAll['total'] += summary['document_count']
            summaryAll['confirmed'] += summary['confirmed']
            summaryAll['cancelled'] += summary['cancelled']
            summaryAll['waiting'] += summary['waiting']

        summary_data['collection_data'].append(summary)

    summary_data['summary']= summaryAll

    return jsonify(summary_data)