import datetime

import discord

from sql import get_db
from sql.models.leaderboard import LeaderboardCategory, LeaderboardScore


async def get_category(category: str) -> LeaderboardCategory:
    """Get a category by name.

    Args:
        category (str): The name of the category to get.

    Returns:
        LeaderboardCategory: The category object.
    """
    with get_db() as db:
        category = (
            db.query(LeaderboardCategory)
            .filter(LeaderboardCategory.category_name == category)
            .first()
        )
        return category


async def get_categories() -> list[LeaderboardCategory]:
    """Get all categories.

    Returns:
        list[LeaderboardCategory]: A list of all categories.
    """
    with get_db() as db:
        return db.query(LeaderboardCategory).all()


async def get_category_names(ctx: discord.ApplicationContext) -> list[str]:
    """Get all category names.

    Args:
        ctx (discord.ApplicationContext): The command context.

    Returns:
        list[str]: A list of all category names.
    """
    with get_db() as db:
        categories = db.query(LeaderboardCategory).all()
        return [category.category_name for category in categories]


async def add_category(category: str, description: str) -> None:
    """Add a category to the leaderboard.

    Args:
        category (str): The name of the category to add.
        description (str): The description of the category.
    """
    with get_db() as db:
        cat = LeaderboardCategory(category_name=category, description=description)
        db.add(cat)
        db.commit()


async def remove_category(category: str) -> None:
    """Remove a category from the leaderboard.

    Args:
        category (str): The name of the category to remove.
    """
    with get_db() as db:
        cat = (
            db.query(LeaderboardCategory)
            .filter(LeaderboardCategory.category_name == category)
            .first()
        )
        db.delete(cat)
        db.commit()


async def get_scores(category: str) -> list[LeaderboardScore]:
    """Get all scores for a category.

    Args:
        category (str): The name of the category to get scores for.

    Returns:
        list[LeaderboardScore]: A list of all scores for the category.
    """
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


async def add_score(msg_id: int, user_id: int, score: float, url: str, category: str) -> bool:
    """Add a score to the leaderboard.

    Args:
        msg_id (int): ID of the message object.
        user_id (int): ID of the user.
        score (float): Score being added.
        url (str): URL of the proof.
        category (str): Category of the score.

    Returns:
        bool: True if the score was added, False otherwise.
    """
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
