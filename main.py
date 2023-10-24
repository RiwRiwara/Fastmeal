from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from Backend.api.Default import defaultAPI
from Backend.api.Components import componentsAPI
from Backend.api.Users import userAPI
from Backend.Constant import Constants

app = Flask(__name__)
CORS(app)
app.template_folder = 'Frontend/templates'
app.static_folder = 'Frontend/static'
app.secret_key = Constants["SECRET_KEY"]

app.register_blueprint(defaultAPI, url_prefix='/')
app.register_blueprint(componentsAPI, url_prefix='/components') 
app.register_blueprint(userAPI, url_prefix='/users') 


if __name__ == '__main__':
    app.run(host=Constants["HOST"], port=Constants["PORT"], debug=True)
