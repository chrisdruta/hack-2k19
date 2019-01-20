from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import face_detect
from PillDispense import dispenser
from api_client import APIClient
import dateutil.parser

from datetime import datetime

app = Flask(__name__)
ask = Ask(app, "/")

baseUrl = "insert aws ip here"
client = APIClient(baseUrl)

# @scott api client example
# response is a dictionary containing the data you want with arbitrary keys.
# What ever you data you want to get or update just follow the patterns below.

# Get list of pill logs
response = client.send_get('pills/logs')
countPills = 0
for medicationLog in response['logs']:
    # Can do date checking
    datetimeObj = dateutil.parser.parse(medicationLog['date'])
    countPills += medicationLog['red']
    countPills += medicationLog['blue']

# Get total pill count
response = client.send_get('pills/count')
totalCount = response['count']

# Get specific pill count
response = client.send_get('pills/count/red')
redCount = response['count']

# Add a new log dictionary containing data, which also updates pill counts
client.send_post('pills/logs', {
    'date': f"{datetime.now().isoformat()}Z",
    'pills': {
        'red': 1,
        'blue': 1
    }
})

# Still need to plan prescriptions
client.get_post('prescription')

# ask: opens on launch of app
@ask.launch
def launch_dispense():
    msg = render_template('get_name')
    return question(msg)

# ask: welcome user
@ask.intent("welcome_user")
def welcome_user(username):
    # INSERT FUNCTION TO CHECK USER NAME
    # client.username = None
    # response = client.send_post('account', {'username': username})
    # userFound = response['success']
    userFound = True
    if userFound:
        msg = render_template('welcome_user')
        #client.username = username
    else:
        msg = render_template('user_not_found')
    return question(msg)


@ask.intent("yes_open_dispense")
# Function to run dispesing function when user says yes
def run_dispense():
    # check for face
    cam = face_detect.faceDetector()
    faceFound = cam.face_scan()
    
    if faceFound:
        # INSERT DISPENSE FUNCTION HERE
        disp = dispenser()
        disp.dispense(1,3)
        msg = render_template('runs_dispense')
    else:
        msg = render_template('no_face')
    return statement(msg)

@ask.intent("no_open_dispense")
# Function to run dispesing function when user says yes
def dont_run_dispense():
    msg = render_template('dont_dispense')
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
