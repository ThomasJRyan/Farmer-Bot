import discord

from sql import get_db
from sql.models.faq import FAQ

async def get_faq(tag: str) -> FAQ:
    """Get a FAQ by tag.

    Args:
        tag (str): The tag of the FAQ to get.

    Returns:
        FAQ: The FAQ object.
    """
    with get_db() as db:
        faq = db.query(FAQ).filter(FAQ.tag == tag).first()
        return faq
    
async def add_faq(tag: str, question: str, answer: str) -> None:
    """Add a FAQ to the database.

    Args:
        tag (str): The tag of the FAQ.
        question (str): The question of the FAQ.
        answer (str): The answer of the FAQ.
    """
    with get_db() as db:
        faq = FAQ(tag=tag, question=question, answer=answer)
        db.add(faq)
        db.commit()
        
async def get_tags(ctx) -> list[str]:
    """Get all FAQ tags.

    Returns:
        list[str]: A list of all FAQ tags.
    """
    with get_db() as db:
        faqs = db.query(FAQ).all()
        return [faq.tag for faq in faqs]