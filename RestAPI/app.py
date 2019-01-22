# basic api bundle for a single path, backed up with the
# inbuilt database, all in one

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from resources import *
from models import *


app = Flask(__name__)
api = Api(app)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')

if __name__ == "__main__":
    app.run(port=5553, debug=True)  # any port can be used here
