import cv2
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera
from flask import Flask, render_template, request, session, logging, url_for, redirect, flash, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_mail import Mail, Message

from passlib.hash import sha256_crypt

from camera import Camera

ekisi = 0

engine = create_engine("sqlite:///database.sqlite")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'autogateapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'autogate123'

mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            surname = request.form.get("surname")
            email = request.form.get("email")
            number_plate_one = request.form.get("number_plate_one")
            number_plate_two = request.form.get("number_plate_two")
            number_plate_three = request.form.get("number_plate_three")
            number_plate_four = request.form.get("number_plate_four")
            carlicense = request.form.get("carlicense")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            security_question = request.form.get("question")
            security_answer = request.form.get("answer")
            secure_password = sha256_crypt.encrypt(str(password))

            name = name.capitalize()
            surname = surname.capitalize()
            number_plate_one = number_plate_one.capitalize()
            number_plate_two = number_plate_two.capitalize()
            number_plate_three = number_plate_three.capitalize()
            security_answer = security_answer.capitalize()
            funds = 0

            car_list = [number_plate_one, number_plate_two, number_plate_three, number_plate_four]

            emaill = db.execute("SELECT email FROM users WHERE email = :email", {"email":email}).fetchone()

            if password == confirm:
                if emaill is None:
                    db.execute("INSERT INTO users(name, surname, email, funds, hpassword)VALUES(:name, :surname, :email, :funds, :hpassword)",
                                {"name":name, "surname":surname, "email":email, "funds":funds, "hpassword":secure_password})
                    db.execute("INSERT INTO passwords(email, question, answer, password)VALUES(:email, :question, :answer, :password)",
                                {"email":email, "password":password, "question":security_question, "answer":security_answer})

                    for regnum in car_list:
                        db.execute("INSERT INTO cars(regnum, carlicense, owner)VALUES(:regnum, :carlicense, :owner)",
                                    {"regnum":regnum, "carlicense":carlicense, "owner":email})

                    db.commit()

                    msg = Message('Welcome to AutoGate', sender = 'autogateapp@gmail.com', recipients = [email])
                    msg.body = "Hie " + name + " " + surname + "! \n\n Your AutoGate account has been successfully created. Welcome to Automated Tollgate Payment System. \n\nRegards, \n\nThe AutoGate Team"
                    mail.send(msg)

                else:
                    messagess = "Email address already exists"
                    return render_template("error.html", messagess = messagess)
                return redirect(url_for('signin'))
            else:
                messagess = "Password does not match"
                return render_template("error.html", messagess = messagess)

        except ConnectionError as e:
            messagess = "Connection Error. Check your internet connection and try again."
            return render_template("error.html", messagess = messagess)
        except Exception as e:
            messagess = "Sorry, something went wrong. Please try again."
            return render_template("error.html", messagess = e)

    return render_template("signup.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/welcome", methods = ["GET", "POST"])
def welcome():
    if request.method == "POST":
        try:
            emails = request.form.get("username")
            passwords = request.form.get("pword")
            email_data = db.execute("SELECT email FROM users WHERE email = :email", {"email":emails}).fetchone()
            password_data = db.execute("SELECT hpassword FROM users WHERE email = :email", {"email":emails}).fetchone()

            if email_data is None:
                messagess = "E-mail address not found"
                return render_template("error.html", messagess = messagess)
            else:
                for pass_data in password_data:
                    if sha256_crypt.verify(passwords, pass_data):
                        name_db = db.execute("SELECT name FROM users WHERE email = :email", {"email":emails}).fetchone()
                        funds_db = db.execute("SELECT funds FROM users WHERE email = :email", {"email":emails}).fetchone()
                        license_db = db.execute("SELECT carlicense FROM cars WHERE owner = :owner", {"owner":emails}).fetchone()
                        nm = name_db[0]
                        funds = funds_db[0]
                        license = license_db[0]

                        return render_template("welcome.html", nm = nm, funds = funds, license = license)
                    else:
                         messagess = "Incorrect Password"
                         return render_template("error.html", messagess = messagess)

        except ConnectionError as e:
            messagess = "Connection Error. Check your internet connection and try again."
            return render_template("error.html", messagess = messagess)
        except Exception as e:
            messagess = "Sorry, something went wrong. Please try again."
            return render_template("error.html", messagess = messagess)

    return render_template("welcome.html", nm = nm, funds = funds, license = license)


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
                messagess = "E-mail Address Not Found"
                return render_template("error.html", messagess = messagess)
            else:
                quest = quest_db[0]

        except ConnectionError as e:
            messagess = "Connection Error. Check your internet connection and try again."
            return render_template("error.html", messagess = messagess)
        except Exception as e:
            messagess = "Sorry, something went wrong. Please try again."
            return render_template("error.html", messagess = messagess)

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
                messagess = "Answer is Incorrect"
                return render_template("error.html", messagess = messagess)

        except ConnectionError as e:
            messagess = "Connection Error. Check your internet connection and try again."
            return render_template("error.html", messagess = messagess)
        except Exception as e:
            messagess = "Sorry, something went wrong. Please try again."
            return render_template("error.html", messagess = messagess)

    return render_template("password.html", e_mail = e_mail)

@app.route("/scan", methods = ["GET", "POST"])
def scan():
        try:
            camera = PiCamera()
            camera.resolution = (640, 480)
            camera.framerate = 30

            rawCapture = PiRGBArray(camera, size=(640, 480))

            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            	image = frame.array
            	cv2.imshow("Frame", image)
            	key = cv2.waitKey(1) & 0xFF

            	rawCapture.truncate(0)

            	if key == ord("s"):
            		text = pytesseract.image_to_string(image)
            		print(text)
            		cv2.imshow("Frame", image)
            		cv2.waitKey(0)
            		break

            cv2.destroyAllWindows()

            email_db = db.execute("SELECT owner FROM cars WHERE regnum = :regnum", {"regnum":text}).fetchone()
            email = email_db[0]
            balance_db = db.execute("SELECT funds FROM users WHERE email = :email" , {"email":email}).fetchone()
            balance = balance_db[0]

            if balance is not None:
                balance = balance - 100
                db.execute("UPDATE users SET funds = :funds WHERE email = :email" , {"funds":balance, "email":email})
                return redirect(url_for('scan'))

        except Exception as e:
            messagess = "Sorry, something went wrong. Please try again."
            return render_template("error.html", messagess = messagess)

        return render_template("scan.html", text = text)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera-test')
def camera_test():
    ekisi = ekisi + 1
    print("")
    print("ekisi:")
    print(ekisi)
    print("")
    return render_template('camera-test.html')



if __name__ == "__main__":
    app.run(debug = True)
    app.secret_key = "autogateapp"
