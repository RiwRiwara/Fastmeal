# Import necessary libraries and modules
from flask import jsonify, request, session, Blueprint ,redirect, url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Backend.Constant import Constants
from . import userAPI
from Backend.db import db
from Backend.api.Users.User import User

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
                session['UserType'] = "customer"
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
    session.pop('UserType', None)
    return redirect(url_for('defaultAPI.index'))
