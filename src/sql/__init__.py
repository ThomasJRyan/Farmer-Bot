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
    global Session
    
    if Session:
        return Session()
    
    Session = sessionmaker(bind=get_engine())
    
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
        
def get_engine():
    """Returns the database engine. Creates one if it
    doesn't already exist.

    Returns:
        Engine: Database engine
    """
    global engine
    
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@database/{MYSQL_DATABASE}?charset=utf8mb4")
    
    return engine