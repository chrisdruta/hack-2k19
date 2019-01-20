from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import face_detect
from PillDispense import dispenser
from api_client import APIClient
import dateutil.parser

from datetime import datetime, timedelta

app = Flask(__name__)
ask = Ask(app, "/")

baseUrl = "insert aws ip here"
client = APIClient(baseUrl)

userFound = False

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

# Get specific prescription
response = client.send_get('prescription/red')
redPrescriptionCount = response['red']

# Still need to plan prescriptions
client.get_post('prescriptions', {
    'pills': {
        'red': 5,
        'blue': 5
    }
})

# ask: opens on launch of app
@ask.launch
def launch_dispense():
    msg = render_template('get_name')
    return question(msg)

# ask: welcome user
@ask.intent("welcome_user")
def welcome_user(username):
    # check for face
    # cam = face_detect.faceDetector()
    # faceFound = cam.face_scan()
    faceFound = True
    if faceFound:
        # check username exsists
        # client.username = None
        # response = client.send_post('account', {'username': username})
        # userFound = response['success']
        userFound = True
        if userFound:
            msg = render_template('welcome_user')
            #client.username = username
        else:
            msg = render_template('user_not_found')
    else:
        msg = render_template('face_not_found')
    return question(msg)

# ask: user wants to take prescription
@ask.intent("user_take_prescription")
def run_dispense():
    if userFound:
        prescriptionTaken = False
        requestTime = datetime.now()

        # iterate through logs to find if perscrition taken
        response = client.send_get('pills/logs')
        for medicationLog in response['logs']:
            prescription = medicationLog['prescription']
            if prescription:
                logTime = dateutil.parser.parse(medicationLog['date'])
                diffTime = (requestTime - logTime).days
                if diffTime >= 1:
                    prescriptionTaken = False
                            
        if prescriptionTaken:
            msg = render_template('taken_prescrip')
        else:
            msg = render_template('not_taken_prescrip')
            # FUNCTION TO UPDATE LOG
            # RUN DISPENSING FUNCTION
    return question(msg)

#ask: user hurts red
@ask.intent("user_needs_pills")
def needs_pills():
    requestTime = datetime.now()

    # iterate through logs to find number of pills taken
    response = client.send_get('pills/logs')
    redT = 0
    for medicationLog in response['logs']:
        logTime = dateutil.parser.parse(medicationLog['date'])
        diffTime = (requestTime - logTime).days
        if diffTime < 1:
            redT += medicationLog['red']
    
    response = client.send_get('prescription/red')
    redP = response['red']

    if redT < redP + 2:
        redD = 1
        msg = render_template('dispense_red')
        # FUNCTION TO UPDATE LOG
        # DISPENSE RED PILL
    else:
        msg = render_template('dont_dispense_red')

    return question(msg)

#ask: user says no
@ask.intent("no_intent")
def user_no():
    msg = render_template('no_intent')
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
