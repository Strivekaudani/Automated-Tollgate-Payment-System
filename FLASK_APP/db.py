
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:////home/pi/clayton/FLASK_APP/database.sqlite3")
db = scoped_session(sessionmaker(bind=engine))