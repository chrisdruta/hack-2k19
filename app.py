from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import face_detect
from PillDispense import dispenser

app = Flask(__name__)
ask = Ask(app, "/")

userFound = False

# ask: opens on launch of app
@ask.launch
def launch_dispense():
    msg = render_template('get_name')
    return question(msg)

# ask: welcome user
@ask.intent("welcome_user")
def welcome_user(username):
    # INSERT FUNCTION TO CHECK USER NAME
    userFound = True
    if userFound:
        msg = render_template('welcome_user')
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
