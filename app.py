from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo

from resources.user import User
from resources.device import Device

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/database"

api = Api(app)
app.mongo = PyMongo(app)

class Hi(Resource):
    def get(self):
        return {'hi': 'fam'}

api.add_resource(Hi, '/')
api.add_resource(User, '/user')
api.add_resource(Device, '/device')


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
