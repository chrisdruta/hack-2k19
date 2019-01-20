from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from sonic import dispenser
from api_client import APIClient
import dateutil.parser
from datetime import datetime, timedelta


app = Flask(__name__)
ask = Ask(app, "/")

baseUrl = "http://34.218.74.17:5000"
client = APIClient(baseUrl)

def stringifyDate(date):
    return date.isoformat()

# ask: opens on launch of app
@ask.launch
def launch_dispense():
    msg = render_template('get_name')
    return question(msg)

# ask: welcome user
@ask.intent("welcome_user")
def welcome_user(username):
    # check username exsists
    client.username = None
    response = client.send_post('account', {'username': username})
    userFound = response['success']
    if userFound:
        msg = render_template('welcome_user', username=username)
        client.username = username
    else:
        msg = render_template('user_not_found', username=username)
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
                if diffTime <= 1:
                    print(diffTime)
                    prescriptionTaken = True
                            
        if prescriptionTaken:
            msg = render_template('taken_prescrip')
        else:
            response = client.send_get('prescription')
            redP = response['red']
            blueP = response['blue']
            print("dispensing")
            disp = dispenser()
            disp.dispense(1, redP)
            disp.dispense(2, blueP)
            #PUT WHILE LOOP HERE
            msg = render_template('not_taken_prescrip')
            client.send_post('logs',{
                'red':redP,
                'blue':blueP,
                'time':stringifyDate(requestTime),
                'isPrescription':True
            })
    else:
        msg = render_template('need_name')
    return question(msg)

#ask: user hurts red
@ask.intent("user_needs_pills_red")
def needs_red_pills():
    if client.username:
        requestTime = datetime.now()

        # iterate through logs to find number of pills taken
        response = client.send_get('logs')
        redT = 0
        for medicationLog in response['logs']:
            logTime = dateutil.parser.parse(medicationLog['time'])
            diffTime = (requestTime - logTime).days
            if diffTime < 1:
                redT += medicationLog['red']
        
        response = client.send_get('prescription')
        redP = response['red']

        if redT < redP + 2:
            redD = 1
            print("dispensing")
            disp = dispenser()
            disp.dispense(1,redD)
            # INSERT WHILE LOOP HERE
            msg = render_template('dispense_red')
            client.send_post('logs',{
                'red':redD,
                'blue':0,
                'time':stringifyDate(requestTime),
                'isPrescription':False
            })            
        else:
            msg = render_template('dont_dispense_red')
    else:
        msg = render_template('need_name')
    return question(msg)

#ask: user hurts blue
@ask.intent("user_needs_pills_blue")
def needs_blue_pills():
    if client.username:
        requestTime = datetime.now()

        # iterate through logs to find number of pills taken
        response = client.send_get('logs')
        blueT = 0
        for medicationLog in response['logs']:
            logTime = dateutil.parser.parse(medicationLog['time'])
            diffTime = (requestTime - logTime).days
            if diffTime < 1:
                blueT += medicationLog['blue']
        
        response = client.send_get('prescription')
        blueP = response['blue']

        if blueT < blueP + 2:
            blueD = 1
            print("dispensing")
            disp = dispenser()
            disp.dispense(2,blueD)
            # INSERT WHILE LOOP HERE
            msg = render_template('dispense_blue')
            client.send_post('logs',{
                'red':0,
                'blue':blueD,
                'time':stringifyDate(requestTime),
                'isPrescription':False
            })       
        else:
            msg = render_template('dont_dispense_blue')
    else:
        msg = render_template('need_name')
    return question(msg)

#ask: has user taken pills
@ask.intent("has_user_taken")
def has_user_taken(username):
    orginal = client.username
    if orginal:
        client.username = None
        response = client.send_post('account', {'username': username})
        userFound = response['success']
        if userFound:
            client.username = username

            prescriptionTaken = False
            requestTime = datetime.now()

            # iterate through logs to find if perscrition taken
            response = client.send_get('logs')
            for medicationLog in response['logs']:
            prescription = medicationLog['isPrescription']
            if prescription:
                logTime = dateutil.parser.parse(medicationLog['time'])
                diffTime = (requestTime - logTime).days
                if diffTime <= 1:
                    print(diffTime)
                    prescriptionTaken = True

            if prescriptionTaken:
                msg = render_template('user_has_taken_prescrip')
            else:
                msg = render_template('user_has_not_taken_prescrip')
        else:
            msg = render_template('user_not_found', username=username)
    else:
        msg = render_template('need_name')
    client.username = orginal
    return question(msg)

#ask: user says no
@ask.intent("no_intent")
def user_no():
    msg = render_template('no_intent')
    return statement(msg)

@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    app.run(debug=True)
