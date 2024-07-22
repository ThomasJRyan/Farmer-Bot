import re
import discord

from discord.ext import commands
from discord.commands.context import ApplicationContext

from sql import get_db
from sql.models.leaderboard import LeaderboardCategory, LeaderboardScore, get_categories
from utils.constants import VERIFIER_ROLE


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    leaderboard = discord.SlashCommandGroup(
        name="leaderboard", description="Leaderboard commands"
    )

    @leaderboard.command(name="show", description="View the leaderboard")
    async def show_leaderboard(
        self,
        ctx: ApplicationContext,
        category: discord.Option(
            str, description="The category to view", autocomplete=get_categories
        ),
    ):
        """A command that displays the leaderboard."""
        with get_db() as db:
            category = (
                db.query(LeaderboardCategory)
                .filter(LeaderboardCategory.category_name == category)
                .first()
            )
            scores = (
                db.query(LeaderboardScore)
                .filter(LeaderboardScore.category_id == category.category_id)
                .order_by(LeaderboardScore.score.desc())
                .all()
            )

            if not scores:
                await ctx.respond("No scores found for this category.")
                return

            msg = "```ex\n"
            for i, score in enumerate(scores[:10]):
                user = ctx.guild.get_member(int(score.user_id))
                msg += f"{i+1}. {user.nick.title()} - {score.score}\n"
            msg += "```"

            await ctx.respond(msg)

    categories = leaderboard.create_subgroup(
        name="categories", description="Leaderboard category commands"
    )

    @categories.command(name="add", description="Add a category to the leaderboard")
    async def add_category(
        self, ctx: ApplicationContext, category: str, description: str
    ):
        """A command that adds a category to the leaderboard."""
        # Check if the user has the verifier role
        user = ctx.author
        if VERIFIER_ROLE and VERIFIER_ROLE not in [role.id for role in user.roles]:
            await ctx.respond("You do not have permission to add a category.")
            return
        
        cat = LeaderboardCategory(category_name=category, description=description)
        with get_db() as db:
            db.add(cat)
            db.commit()
        await ctx.respond(f"Added category `{category}` to the leaderboard.")

    @categories.command(
        name="remove", description="Remove a category from the leaderboard"
    )
    async def remove_category(self, ctx: ApplicationContext, category: str):
        """A command that removes a category from the leaderboard."""
        # Check if the user has the verifier role
        user = ctx.author
        if VERIFIER_ROLE and VERIFIER_ROLE not in [role.id for role in user.roles]:
            await ctx.respond("You do not have permission to remove a category.")
            return
        
        with get_db() as db:
            cat = (
                db.query(LeaderboardCategory)
                .filter(LeaderboardCategory.category_name == category)
                .first()
            )
            db.delete(cat)
            db.commit()
        await ctx.respond(f"Removed category `{category}` from the leaderboard.")

    @categories.command(
        name="list", description="List all categories on the leaderboard"
    )
    async def list_categories(self, ctx: ApplicationContext):
        """A command that lists all categories on the leaderboard."""
        with get_db() as db:
            categories = db.query(LeaderboardCategory).all()
            msg = "```protobuf\n"
            for category in categories:
                msg += f"\"{category.category_name}\" - {category.description}\n"
            msg += "```"
            await ctx.respond(msg)


def setup(bot):
    bot.add_cog(Leaderboard(bot))
