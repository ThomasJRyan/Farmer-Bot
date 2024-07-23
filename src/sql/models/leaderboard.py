import discord

from sqlalchemy import Column, Integer, String, Float, ForeignKey, BigInteger, Boolean, Time
from sqlalchemy.orm import declarative_base, relationship

from sql import get_db, get_engine

Base = declarative_base()


class LeaderboardCategory(Base):
    __tablename__ = "leaderboard_categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(256), primary_key=True)
    description = Column(String(256))
    deprecated = Column(Boolean, default=False)


class LeaderboardScore(Base):
    __tablename__ = "leaderboard_scores"

    msg_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    score = Column(Float)
    url = Column(String(256))
    category_id = Column(Integer, ForeignKey("leaderboard_categories.category_id"))
    category = relationship("LeaderboardCategory", backref="leaderboard_scores")
    timestamp = Column(Time)


LeaderboardCategory.__table__.create(get_engine(), checkfirst=True)
LeaderboardScore.__table__.create(get_engine(), checkfirst=True)


def add_default_categories():
    DEFAULT_CATEGORIES = [
        ("60s: Hay", "Collect as much hay as you can in 60 seconds."),
        ("60s: Wood", "Collect as much wood as you can in 60 seconds."),
        ("60s: Carrots", "Collect as many carrots as you can in 60 seconds."),
        ("60s: Pumpkins", "Collect as many pumpkins as you can in 60 seconds."),
        ("60s: Power", "Collect as much power as you can in 60 seconds."),
        ("60s: Gold", "Collect as much gold as you can in 60 seconds."),
        ("60s: Cactus", "Collect as many cacti as you can in 60 seconds."),
        ("60s: Bones", "Collect as many bones as you can in 60 seconds."),
        ("Maze: 300", "Complete the maze 300 times as fast as you can."),
        ("Maze: 100", "Complete the maze 100 times as fast as you can."),
        ("Maze: 200 8x8", "Complete the 8x8 maze 200 times as fast as you can."),
        ("Maze: 10x20", "Complete the 10x20 maze as fast as you can."),
    ]

    with get_db() as db:
        for category, description in DEFAULT_CATEGORIES:
            cat = (
                db.query(LeaderboardCategory)
                .filter(LeaderboardCategory.category_name == category)
                .first()
            )
            if not cat:
                lb = LeaderboardCategory(category_name=category, description=description)
                db.add(lb)
                db.commit()

add_default_categories()