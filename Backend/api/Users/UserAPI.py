# Import necessary libraries and modules
from flask import jsonify, request, session, Blueprint ,redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Backend.Constant import Constants
from . import userAPI
from Backend.db import db
from Backend.api.Users.User import User
from bson import ObjectId 

def get_next_user_id():
    sequence_doc = db.counters.find_one_and_update(
        {'_id': 'user_item_id'},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    if sequence_doc:
        return sequence_doc['seq']
    else:
        db.counters.insert_one({'_id': 'user_item_id', 'seq': 1})
# Create a function for user signup
@userAPI.route('/signup', methods=['POST'])
def user_signup():
    try:
        if request.is_json:
            user_data = request.json
        else:
            user_data = request.form.to_dict()
            
        existing_user = db.users.find_one({"email": user_data['email']})

        if existing_user:
            return jsonify({"message": "User with this email already exists"}), 400

        email = user_data.get('email')
        phone = user_data.get('phone')
        name = user_data.get('name')
        password = user_data.get('password')

        new_user = User(id=None, name=name, email=email, password=password, role="Customer", phone=phone)
        user_data = new_user.getJson()
        user_data['address'] = "<please edit address>"
        user_data['role'] = "customer"
        user_data['id'] = get_next_user_id()

        user_id = db.users.insert_one(user_data).inserted_id
        if request.is_json:
            return jsonify({"message": "User signed up successfully", "user_id": str(user_id)}), 201
        else:
            return redirect(url_for('defaultAPI.index'))
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Create a function for user sign-in
@userAPI.route('/signin', methods=['POST'])
def user_signin():
    try:
        if request.is_json:
            user_credentials = request.json
            email = user_credentials.get('email')
            password = user_credentials.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            print(request.form)

        user = db.users.find_one({"email": email})

        if user:
            if user['password'] == password:
                user['_id'] = str(user['_id'])
                user.pop("password", None)
                session['IsUserLoggedIn'] = True
                if db.users.find_one({"email": email})['role']:
                    session['UserType'] = db.users.find_one({"email": email})['role']
                else:
                    session['UserType'] = "customer"
                session['email'] = email
                
                if request.is_json:
                    return jsonify({"message": "User signed in successfully", "user_data": user}), 200
                else:
                    return redirect(url_for('defaultAPI.index'))
            else:
                return jsonify({"message": "Invalid email or password"}), 401
        else:
            return jsonify({"message": "User account not found"}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 500

@userAPI.route('/logout')
def logout():
    session.pop('isUserLoggedIn', None)
    session.pop('IsUserLoggedIn', None)
    session.pop('email', None)
    session.pop('UserType', None)
    session.pop('cart_items', None)
    return redirect(url_for('defaultAPI.index'))

@userAPI.route('/update', methods=['POST'])
def update_user_data_by_email():
    try:
        if request.is_json:
            user_update_data = request.json
        else:
            user_update_data = request.form.to_dict()

        email = session.get('email', None)

        user = db.users.find_one({"email": email})

        if not user:
            return jsonify({"message": "User not found"}), 404

        user_update_data.pop('comment', None)

        for key, value in user_update_data.items():
            user[key] = value


        db.users.update_one({"email": email}, {"$set": user})


        return jsonify({"message": "User data updated successfully"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500





