import os
import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')


engine = None
Session = None

def create_session():
    """Creates a global session for the database. If one
    doesn't already exist. If one does exist, it returns
    that session.

    Returns:
        Session: Database session
    """
    global engine
    global Session
    
    if Session:
        return Session()
    
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@database/{MYSQL_DATABASE}?charset=utf8mb4")
    
    Session = sessionmaker(bind=engine)
    
    return Session()

@contextlib.contextmanager
def get_db():
    """Yields a session for the database.
    Ensures that the session is closed after the
    context manager is done.

    Yields:
        Session: Database session
    """
    session = create_session()
    try:
        yield session
    finally:
        session.close()