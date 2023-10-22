from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Backend.Constant import Constants

uri = Constants["MONGODB_URL"]
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[Constants["MONGODB_DB"]]
