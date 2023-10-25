from . import defaultAPI
from flask import  jsonify, render_template, request, session, redirect, url_for
import json
from Backend.Constant import Constants
from Backend.db import db
from werkzeug.exceptions import BadRequest

def get_next_food_id():
    sequence_doc = db.counters.find_one_and_update(
        {'_id': 'food_item_id'},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    if sequence_doc:
        return sequence_doc['seq']
    else:
        db.counters.insert_one({'_id': 'food_item_id', 'seq': 1})
        return 1
    
@defaultAPI.route('/food-test', methods=['GET'])
def api_food_entry():
    response = {
        'data': "Food API Running"
    }
    return jsonify(response)

@defaultAPI.route('/food/create', methods=['POST'])
def create_or_update_food():
    if request.method == 'POST':
        data = request.get_json()

        if 'name' in data and 'price' in data and 'id' not in data:
            food_id = get_next_food_id()
            data['id'] = str(food_id)
            db.food_items.insert_one(data)
            return jsonify({'message': f'Food item with ID {food_id} created successfully'}, 201)
        elif 'id' in data:
            updated_id = data['id']
            del data['id']  # Remove the 'id' field from the data since we don't want to update it
            db.food_items.update_one({'id': updated_id}, {'$set': data})
            return jsonify({'message': f'Food item with ID {updated_id} updated successfully'}, 200)
        else:
            return jsonify({'error': 'Missing required fields'}, 400)


@defaultAPI.route('/food', methods=['GET'])
def get_food_list():
    food_name = request.args.get('name')
    food_id = request.args.get('id')
    filter_dict = {}
    if food_name:
        filter_dict['name'] = {'$regex': food_name, '$options': 'i'}
    if food_id:
        filter_dict['id'] = food_id
    food_list = list(db.food_items.find(filter_dict, {'_id': 0}))
    print(food_list)

    if food_list:
        return jsonify(food_list)
    else:
        return jsonify({'message': 'No matching food items found'}, 404)


@defaultAPI.route('/food/delete/<string:food_id>', methods=['DELETE'])
def delete_food(food_id):
    result = db.food_items.delete_one({'id': food_id})

    if result.deleted_count > 0:
        return jsonify({'message': f'Food item with ID {food_id} deleted successfully'}, 200)
    else:
        return jsonify({'error': f'Food item with ID {food_id} not found'}, 404)


@defaultAPI.route('/food/cancel_cart', methods=['POST'])
def cancel_cart():
    session.pop('cart_items', None)
    return jsonify({'message': 'Cart cleared successfully'}), 200

@defaultAPI.route('/food/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        if request.is_json:
            food_data = request.json
            food_id = food_data.get('id')
            food_quantity = food_data.get('quantity')

            if not food_id or not food_quantity or food_quantity <= 0:
                raise BadRequest('Invalid food_id or quantity')

            cart_items = session.get('cart_items', {})
            if food_id in cart_items:
                cart_items[food_id]['quantity'] += food_quantity
            else:
                cart_items[food_id] = {'quantity': food_quantity}

            session['cart_items'] = cart_items
            session.modified = True  # To ensure the session is saved

            return jsonify({'message': 'Item added to cart successfully'}), 200

        else:
            raise BadRequest('Invalid request')
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400