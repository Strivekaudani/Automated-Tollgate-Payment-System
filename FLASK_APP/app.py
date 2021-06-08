# import cv2
# import pytesseract
# from picamera.array import PiRGBArray
# from picamera import PiCamera
from flask import Flask, render_template, request, session, logging, url_for, redirect, flash, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from flask_mail import Mail, Message

from utils import Response

# from passlib.hash import sha256_crypt
# from camera import Camera

# from db import db

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'autogateapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'autogate123'

app.debug = True
app.host = '192.168.0.113'
app.reload = True;

# mail = Mail(app)


# route handlers
from create_account import create_account
from payments import add_funds, approve_funds, remove_payment
from sign_in import sign_in
from dashboards import admin_dashboard, user_dashboard
from cars import pay_for_this_car


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/notice')
def notice():
    message = request.args.get('message')
    return render_template('notice.html', message = message)


@app.route('/admin-dashboard')
def admin():
    response = Response(request)
    return admin_dashboard(request, response)

@app.route('/user-dashboard', methods = [ 'GET', 'POST' ])
def user():
    response = Response(request)
    return user_dashboard(request, response)



@app.route("/signup", methods = ["POST", "GET"])
def signup():

    response = Response(request)

    if (request.method == 'POST'):
        return create_account(request, response)
    else:
        return render_template('signup.html')


@app.route("/signin", methods = [ "GET", "POST" ])
def signin():

    response = Response(request)
    if (request.method == 'GET'):
        return render_template("signin.html")
    else:
        return sign_in(request, response)

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/recover", methods = ["GET", "POST"])
def recover():
    if request.method == "POST":
        try:
            emai = request.form.get("username")
            quest_db = db.execute("SELECT question FROM passwords WHERE email = :email", {"email":emai}).fetchone()

            if quest_db is None:
                error_msg = "E-mail Address Not Found"
                return render_template("error.html", error_msg = error_msg)
            else:
                quest = quest_db[0]

        except ConnectionError as e:
            error_msg = "Connection Error. Check your internet connection and try again."
            return render_template("error.html", error_msg = error_msg)
        except Exception as e:
            error_msg = "Sorry, something went wrong. Please try again."
            return render_template("error.html", error_msg = error_msg)

    return render_template("recover.html", quest = quest)

@app.route("/password", methods = ["GET", "POST"])
def password():
    if request.method == "POST":
        try:
            ans = request.form.get("answers")
            ans = ans.capitalize()
            e_mail = request.form.get("mail")
            answer_db = db.execute("SELECT answer FROM passwords WHERE email = :email", {"email":e_mail}).fetchone()
            ans_wer = answer_db[0]

            if ans == ans_wer:
                passs = db.execute("SELECT password FROM passwords WHERE answer = :answer", {"answer":ans}).fetchone()
                paass = passs[0]

                nom_db = db.execute("SELECT name FROM users WHERE email = :email" , {"email":e_mail}).fetchone()
                nom = nom_db[0]
                surnom_db = db.execute("SELECT surname FROM users WHERE email = :email" , {"email":e_mail}).fetchone()
                surnom = surnom_db[0]

                msg = Message('Password for AutoGate', sender = 'autogateapp@gmail.com', recipients = [e_mail])
                msg.body = "Hie " + nom + " " + surnom + "! The password for your AutoGate account is " + paass + " \n\nRegards, \n\nThe AutoGate Team"
                mail.send(msg)
            else:
                error_msg = "Answer is Incorrect"
                return render_template("error.html", error_msg = error_msg)

        except ConnectionError as e:
            error_msg = "Connection Error. Check your internet connection and try again."
            return render_template("error.html", error_msg = error_msg)
        except Exception as e:
            error_msg = "Sorry, something went wrong. Please try again."
            return render_template("error.html", error_msg = error_msg)

    return render_template("password.html", e_mail = e_mail)

@app.route("/scan", methods = ["GET", "POST"])
def scan():

        return render_template("scan.html");

        # try:
        #     camera = PiCamera()
        #     camera.resolution = (640, 480)
        #     camera.framerate = 30

        #     rawCapture = PiRGBArray(camera, size=(640, 480))

        #     for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #     	image = frame.array
        #     	cv2.imshow("Frame", image)
        #     	key = cv2.waitKey(1) & 0xFF

        #     	rawCapture.truncate(0)

        #     	if key == ord("s"):
        #     		text = pytesseract.image_to_string(image)
        #     		print(text)
        #     		cv2.imshow("Frame", image)
        #     		cv2.waitKey(0)
        #     		break

        #     cv2.destroyAllWindows()

        #     email_db = db.execute("SELECT owner FROM cars WHERE regnum = :regnum", {"regnum":text}).fetchone()
        #     email = email_db[0]
        #     balance_db = db.execute("SELECT funds FROM users WHERE email = :email" , {"email":email}).fetchone()
        #     balance = balance_db[0]

        #     if balance is not None:
        #         balance = balance - 100
        #         db.execute("UPDATE users SET funds = :funds WHERE email = :email" , {"funds":balance, "email":email})
        #         return redirect(url_for('scan'))

        # except Exception as e:
        #     error_msg = "Sorry, something went wrong. Please try again."
        #     return render_template("error.html", error_msg = error_msg)

        # return render_template("scan.html", text = text)


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video-feed')
# def video_feed():
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')



# ============================================================================================
# API ROUTES
# ============================================================================================

@app.route('/api/cars/<number_plate>/payment', methods = [ 'GET', 'POST' ])
def pay_for_car(number_plate):
    request.params = { 'number_plate': number_plate };
    response = Response(request)
    return pay_for_this_car(request, response)


# ============================================================================================
# PAYMENT ROUTES
# ============================================================================================

@app.route('/add-funds', methods = [ "POST" ])
def funds():
    response = Response(request)
    return add_funds(request, response)


@app.route('/approve-payment', methods = [ 'POST' ])
def _approve_funds():
    response = Response(request)
    return approve_funds(request, response)

@app.route('/remove-payment', methods = [ 'POST' ])
def _remove_payment():
    response = Response(request)
    return remove_payment(request, response)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    app.secret_key = "autogateapp"


