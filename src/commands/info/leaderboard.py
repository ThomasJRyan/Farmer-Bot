import discord

from discord.ext import commands
from discord.commands.context import ApplicationContext

from sql.crud.leaderboard import (
    get_categories,
    get_category_names,
    add_category,
    remove_category,
    get_scores,
)
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
            str, description="The category to view", autocomplete=get_category_names
        ), # type: ignore
    ):
        """A command that displays the leaderboard."""
        scores = await get_scores(category)

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
    @commands.has_role(VERIFIER_ROLE)
    async def add_category(
        self, ctx: ApplicationContext, category: str, description: str
    ):
        """A command that adds a category to the leaderboard."""
        await add_category(category, description)
        await ctx.respond(f"Added category `{category}` to the leaderboard.")

    @categories.command(
        name="remove", description="Remove a category from the leaderboard",
    )
    @commands.has_role(VERIFIER_ROLE)
    async def remove_category(
        self,
        ctx: ApplicationContext,
        category: discord.Option(
            str, description="The category to view", autocomplete=get_category_names
        ), # type: ignore
    ):
        """A command that removes a category from the leaderboard."""
        await remove_category(category)
        await ctx.respond(f"Removed category `{category}` from the leaderboard.")

    @categories.command(
        name="list", description="List all categories on the leaderboard"
    )
    async def list_categories(self, ctx: ApplicationContext):
        """A command that lists all categories on the leaderboard."""
        categories = await get_categories()
        msg = "```protobuf\n"
        for category in categories:
            msg += f'"{category.category_name}" - {category.description}\n'
        msg += "```"
        await ctx.respond(msg)


def setup(bot):
    bot.add_cog(Leaderboard(bot))
