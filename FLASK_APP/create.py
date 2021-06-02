from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///clayton/FLASK_APP/data.sqlite")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/")
def index():

    return "<h1> Successfully Created </h1>"


if __name__ == "__main__":
    app.run(debug = True)
    app.secret_key = "autogateapp"
