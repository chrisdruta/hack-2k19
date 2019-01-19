from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/database"

mongo = PyMongo(app)

@app.route('/post', methods=['GET', 'POST'])
def endpoint():
    
    body

    if request.method == 'POST':
        print(request.get_json())
        return jsonify({'hello': "world"})
    else:
        return jsonify({'hello': "world"})

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

@app.route('/')
