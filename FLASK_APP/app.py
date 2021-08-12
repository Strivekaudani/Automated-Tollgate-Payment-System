
from flask import Flask, render_template, request, session, logging, url_for, redirect, flash, make_response, Response as FlaskResponse
from sqlalchemy import create_engine
from flask_socketio import SocketIO, emit
import os
from subprocess import Popen
from flask_mail import Mail, Message
from utils import Response

# from passlib.hash import sha256_crypt
try:
    from camera import Camera
except:
    from fake_camera import Camera

try:
    os.system('sudo pigpiod');
except:
    pass
    
os.system('clear');

try:
    Popen('python3 autoscan.py', shell=True);
except:
    pass


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'automaticetollgate@gmail.com'
app.config['MAIL_PASSWORD'] = 'qwertyazerty'

app.debug = True
app.host = '192.168.0.100'
app.reload = True;

mail = Mail(app)
socket = SocketIO(app, async_mode=None);


# route handlers
from create_account import create_account
from payments import add_funds, approve_funds, remove_payment, poll_payment
from sign_in import sign_in
from dashboards import admin_dashboard, user_dashboard
from cars import pay_for_car, add_car, remove_car
from boom_gate import open_and_close, open_gate_handler
from scan import scan_plates, auto_scan


@app.route("/")
def index():
    return render_template('index.html', async_mode=socket.async_mode)

@app.route('/logout')
def logout():

    response = Response(request)
    return response.redirect_302('/')


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
        return create_account(request, response, mail)
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

    response = Response(request)

    user = request.user;

    if (user == None):
        return response.redirect_302('/notice?message=You need to login to access this page.');

    is_not_admin = not user["is_admin"];

    if (is_not_admin):
        return response.redirect_302('/notice?message=You are not authorized to access this page.');

    response.body = render_template("scan.html", async_mode=socket.async_mode);
    return response.render();



def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video-feed')
def video_feed():
    return FlaskResponse(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



# ============================================================================================
# API ROUTES
# ============================================================================================

@app.route('/api/open-gate-command', methods = [ "POST" ])
def _open_gate_handler():
    response = Response(request)
    return open_gate_handler(request, response);


@app.route('/api/scanned-plates', methods = [ 'GET' ])
def _scan_plates():
    response = Response(request)
    return scan_plates(request, response);

@app.route('/api/auto-scan-command', methods=[ 'POST' ])
def _auto_scan():
    request.namespace = '/scan'
    response = Response(request)
    return auto_scan(request, response, emit, mail, Message);

# ============================================================================================
# PAYMENT ROUTES
# ============================================================================================

@app.route('/add-funds', methods = [ "POST" ])
def funds():
    response = Response(request)
    return add_funds(request, response, mail, Message)

@app.route('/poll-payment', methods = [ 'GET', 'POST' ])
def _poll_payment():
    response = Response(request)
    return poll_payment(request, response, mail, Message);



@app.route('/approve-payment', methods = [ 'POST' ])
def _approve_funds():
    response = Response(request)
    return approve_funds(request, response)

@app.route('/remove-payment', methods = [ 'POST' ])
def _remove_payment():
    response = Response(request)
    return remove_payment(request, response)

@app.route('/stop')
def stop():

    for sid in text_detectors:
        text_detectors[sid].stop();

    return "DONE\n";

# ============================================================================================
# CAR ROUTES
# ============================================================================================

@app.route('/add-car', methods = [ "POST" ] )
def _add_car():
    response = Response(request)
    return add_car(request, response);

@app.route('/remove-car', methods = [ "POST" ] )
def _remove_car():
    response = Response(request)
    return remove_car(request, response);

@app.route('/pay-for-car', methods = [ "POST" ] )
def _pay_for_car():
    response = Response(request)
    return pay_for_car(request, response);

# ============================================================================================
# WEBSOCKETS
# ============================================================================================


ws_clients = {}
ws_clients['count'] = 0

@socket.on('connect')
def on_ws_connect():
    ws_clients['count'] = ws_clients['count'] + 1

@socket.on('disconnect')
def on_ws_disconnect():
    ws_clients['count'] = ws_clients['count'] - 1

if __name__ == "__main__":
    app.secret_key = "autogateapp"
    app.run(host="0.0.0.0", port=80)
    socket.run(app);
