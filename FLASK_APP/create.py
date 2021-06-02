from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///clayton/FLASK_APP/data.sqlite")
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

@app.route("/")
def index():
    db.execute('CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      name VARCHAR NOT NULL,
      surname VARCHAR NOT NULL,
      email VARCHAR NOT NULL UNIQUE,
      one VARCHAR NOT NULL UNIQUE,
      two VARCHAR NOT NULL UNIQUE,
      three VARCHAR NOT NULL UNIQUE,
      hpassword VARCHAR(100) NOT NULL,
        );
    ')

    db.execute('CREATE TABLE passwords (
      id SERIAL PRIMARY KEY,
      email VARCHAR NOT NULL UNIQUE,
      question VARCHAR NOT NULL,
      answer VARCHAR NOT NULL,
      password VARCHAR NOT NULL,
        );
    ')

    db.execute('CREATE TABLE confirmations (
      id SERIAL PRIMARY KEY,
      email VARCHAR NOT NULL,
      plate VARCHAR NOT NULL,
      amount VARCHAR NOT NULL,
      code VARCHAR NOT NULL,
        );
    ')

    db.execute('CREATE TABLE money (
      id SERIAL PRIMARY KEY,
      email VARCHAR NOT NULL,
      balance INTEGER NOT NULL
        );
    ')

    return "<h1> Successfully Created </h1>"


if __name__ == "__main__":
    app.run(debug = True)
    app.secret_key = "autogateapp"
