import datetime

import discord

from sql import get_db
from sql.models.leaderboard import LeaderboardCategory, LeaderboardScore


async def get_category(category: str):
    with get_db() as db:
        category = (
            db.query(LeaderboardCategory)
            .filter(LeaderboardCategory.category_name == category)
            .first()
        )
        return category


async def get_categories():
    with get_db() as db:
        return db.query(LeaderboardCategory).all()


async def get_category_names(ctx: discord.ApplicationContext):
    with get_db() as db:
        categories = db.query(LeaderboardCategory).all()
        return [category.category_name for category in categories]


async def add_category(category: str, description: str):
    with get_db() as db:
        cat = LeaderboardCategory(category_name=category, description=description)
        db.add(cat)
        db.commit()


async def remove_category(category: str):
    with get_db() as db:
        cat = (
            db.query(LeaderboardCategory)
            .filter(LeaderboardCategory.category_name == category)
            .first()
        )
        db.delete(cat)
        db.commit()


async def get_scores(category: str):
    with get_db() as db:
        category = await get_category(category)
        if not category:
            return None

        scores = (
            db.query(LeaderboardScore)
            .filter(LeaderboardScore.category_id == category.category_id)
            .order_by(LeaderboardScore.score.desc())
            .all()
        )
        return scores


async def add_score(msg_id: int, user_id: int, score: float, url: str, category: str):
    with get_db() as db:
        category = (
            db.query(LeaderboardCategory)
            .filter(LeaderboardCategory.category_name == category)
            .first()
        )
        if not category:
            return False

        score = LeaderboardScore(
            msg_id=msg_id,
            user_id=user_id,
            score=score,
            url=url,
            category_id=category.category_id,
            timestamp=datetime.datetime.now(),
        )
        db.add(score)
        db.commit()
        return True
