from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Backend.api.Default import defaultAPI
from Backend.Constant import Constants

app = Flask(__name__)
CORS(app)
app.template_folder = 'Frontend/templates'
app.static_folder = 'Frontend/static'

app.register_blueprint(defaultAPI, url_prefix='/')


if __name__ == '__main__':
    app.run(host=Constants["HOST"], port=Constants["PORT"], debug=True)
