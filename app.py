from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
# from PillDispense import dispenser
from api_client import APIClient
import dateutil.parser
from datetime import datetime, timedelta

app = Flask(__name__)
ask = Ask(app, "/")

baseUrl = "34.218.74.17:5000"
client = APIClient(baseUrl)

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
        client.username = None
        response = client.send_post('account', {'username': username})
        userFound = response['success']
        if userFound:
            msg = render_template('welcome_user')
            client.username = username
        else:
            msg = render_template('user_not_found')
    else:
        msg = render_template('face_not_found')
    return question(msg)

# ask: user wants to take prescription
@ask.intent("user_take_prescription")
def run_dispense():
    if client.username:
        prescriptionTaken = False
        requestTime = datetime.now()

        # iterate through logs to find if perscrition taken
        response = client.send_get('logs')
        for medicationLog in response['logs']:
            prescription = medicationLog['isPrescription']
            if prescription:
                logTime = dateutil.parser.parse(medicationLog['time'])
                diffTime = (requestTime - logTime).days
                if diffTime >= 1:
                    prescriptionTaken = False
                            
        if prescriptionTaken:
            msg = render_template('taken_prescrip')
        else:
            msg = render_template('not_taken_prescrip')
            response = client.send_get('prescription')
            redP = response['red']
            blueP = response['blue']
            client.send_post('logs',{
                'red':redP,
                'blue':blueP,
                'time':requestTime,
                'isPrescription':True
            })
            print("dispensing")
    else:
        msg = render_template('need_name')
    return question(msg)

#ask: user hurts red
@ask.intent("user_needs_pills")
def needs_pills():
    if client.username:
        requestTime = datetime.now()

        # iterate through logs to find number of pills taken
        response = client.send_get('logs')
        redT = 0
        for medicationLog in response['logs']:
            logTime = dateutil.parser.parse(medicationLog['date'])
            diffTime = (requestTime - logTime).days
            if diffTime < 1:
                redT += medicationLog['red']
        
        response = client.send_get('prescription')
        redP = response['red']

        if redT < redP + 2:
            redD = 1
            msg = render_template('dispense_red')
            client.send_post('logs',{
                'red':redD,
                'blue':0,
                'time':requestTime,
                'isPrescription':False
            })
            print("dispense")
        else:
            msg = render_template('dont_dispense_red')
    else:
        msg = render_template('need_name')
    return question(msg)

#ask: user says no
@ask.intent("no_intent")
def user_no():
    msg = render_template('no_intent')
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=True)
