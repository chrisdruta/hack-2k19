from flask import Flask, request, jsonify

from flask_pymongo import PyMongo
from flask_ask import Ask, statement

import datetime
import json
import os
import logging

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

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

@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("YesIntent")
def next_round():
    numbers = [randint(0, 9) for _ in range(3)]
    round_msg = render_template('round', numbers=numbers)
    session.attributes['numbers'] = numbers[::-1]  # reverse
    return question(round_msg)

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    winning_numbers = session.attributes['numbers']
    if [first, second, third] == winning_numbers:
        msg = render_template('win')
    else:
        msg = render_template('lose')
    return statement(msg)


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
	app.run(debug=True, host='0.0.0.0', ssl_context='adhoc')
