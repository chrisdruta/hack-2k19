from flask import Flask, request, jsonify

from flask_pymongo import PyMongo
from flask_ask import Ask, statement

import datetime
import json
import os

app = Flask(__name__)
ask = Ask(app, '/')

# File IO functions, cuz fuck databases
def load():
    data = None
    try:
        with open('data.json', 'r') as openFile:
            data = json.load(openFile)
    except:
        raise RuntimeError("Failed to load data file")

    if data == None:
        raise RuntimeError("Failed to load data file")
    else:
        return data

def save(data):
    try:
        with open('data.json', 'w') as openFile:
            json.dump(data, openFile)
    except:
        raise RuntimeError("Failed to write data file")

@app.route('/', methods=['GET', 'POST'])
def endpoint():
    return jsonify({'hello': "world"})

# @scott: thing of all the intents and other flask-ask shit
@ask.intent('ShouldTakePills')
def checkPills():
    # Load user data (like in format below)
    data = load()
    # Do stuff with that data, eg check most recent logs in pillLog and make decision
    
    # Tell alexa what to say back

@ask.intent('Remind me in 30s')
def addReminder():
    data = load()
    # update data, eg data['pillCount'] = 48
    save(data)

    # Tell alexa what to say back

@ask.intent('HelloIntent')
def hello(firstname):
    text = render_template('hello', firstname=firstname)
    return statement(text).simple_card('Hello', text)
       
# Example user
user = {
    'pillCount': 50,
    'pillConfigs': [
        {
            'name': "config 1",
            'red': 1,
            'blue': 1
        },
        {
            'name': "config 2",
            'red': 2,
            'blue': 2
        }
    ],
    'defaultPillConfig': 0,
    'pillLog': [
        {
            'date': datetime.datetime.now().timestamp(),
            'pills': {
                'red': 2,
                'blue': 0
            }
        },
        {
            'date': datetime.datetime.now().timestamp(),
            'pills': {
                'red': 5,
                'blue': 10
            }
        }
    ],
    'reminders': [
        {
            'msg': "insert message here",
            'time': "time?"
        }
    ]
}

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
