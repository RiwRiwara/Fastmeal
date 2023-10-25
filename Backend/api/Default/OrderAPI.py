from . import defaultAPI
from flask import  jsonify, render_template, request, session, redirect, url_for
import json
from Backend.Constant import Constants
import datetime
from Backend.db import db

@defaultAPI.route('/order-test', methods=['GET'])
def api_order_entry():
    response = {
        'data': "orders API Running"
    }
    return jsonify(response)

def get_next_order_id():
    sequence_doc = db.counters.find_one_and_update(
        {'_id': 'order_item_id'},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    if sequence_doc:
        return sequence_doc['seq']
    else:
        db.counters.insert_one({'_id': 'order_item_id', 'seq': 1})
        return 1
    

@defaultAPI.route('/order/create', methods=['POST'])
def create_or_update_order():
    if request.method == 'POST':
        data = request.get_json()['order_data']
        if 'email' in data and 'id' not in data and 'food_data' in data:
            data['food_data'] = json.loads(data['food_data'])
            foodsList = []
            for i in data['food_data']:
                foodsList.append(db.food_items.find_one({'id': i}, {'_id': 0}))
            data['food_data'] = foodsList
            order_id = get_next_order_id()
            data['id'] = str(order_id)
            data['status'] = 'waiting'
            data['email'] = str(data['email'])
            data['created_at'] = data['updated_at'] = datetime.datetime.now()

            db.order_items.insert_one(data)
            session.pop('cart_items', None)
            return jsonify({'message': f'order item with ID {order_id} created successfully'}, 201)
        elif 'id' in data:
            updated_id = data['id']
            del data['id'] 
            db.order_items.update_one({'id': updated_id}, {'$set': data})
            return jsonify({'message': f'order item with ID {updated_id} updated successfully'}, 200)
        else:
            return jsonify({'error': 'Missing required fields'}, 400)


@defaultAPI.route('/order', methods=['GET'])
def get_order_list():
    order_id = request.args.get('id')
    email = request.args.get('email')
    filter_dict = {}
    if email:
        filter_dict['email'] = {'$regex':email, '$options': 'i'}
    if order_id:
        filter_dict['id'] = order_id
        print(filter_dict)
    order_list = list(db.order_items.find(filter_dict, {'_id': 0}))

    if order_list:
        return jsonify(order_list)
    else:
        return jsonify({'message': 'No matching order items found'}, 404)


@defaultAPI.route('/order/delete/<string:order_id>', methods=['DELETE'])
def delete_order(order_id):
    result = db.order_items.delete_one({'id': order_id})

    if result.deleted_count > 0:
        return jsonify({'message': f'order item with ID {order_id} deleted successfully'}, 200)
    else:
        return jsonify({'error': f'order item with ID {order_id} not found'}, 404)
