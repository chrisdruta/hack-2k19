from flask import Flask
from flask_restful import Resource, Api

from route.user import User

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/user')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

print("hi dick")
