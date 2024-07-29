from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    BigInteger,
    Boolean,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

from sql import get_db, get_engine

Base = declarative_base()

class FAQ(Base):
    __tablename__ = "faq"

    tag = Column(String(256), primary_key=True, unique=True)
    question = Column(String(256))
    answer = Column(String(2000))

    __table_args__ = (UniqueConstraint('tag'),)
    
FAQ.__table__.create(get_engine(), checkfirst=True)