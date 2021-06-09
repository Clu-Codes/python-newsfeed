from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable

# engine variable manages the overall connection to the database
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)

# session variable generates temporary connections for performing CRUD operations
Session = sessionmaker(bind=engine)

# Base class variable helps map the models to real MySQL tables
Base = declarative_base()

def init_db(app):
    Base.metadata.create_all(engine)

    app.teardown_appcontext(close_db)

def get_db():
    if 'db' not in g:
        # store db connection in app context
        g.db = Session()

    return g.db

# the pop() method attempts to find and remove db from the 'g' object. If db exists (that is, db doesn't equal None), then db.close() ends the connection. 
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()