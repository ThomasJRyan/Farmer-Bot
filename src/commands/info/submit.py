from discord.ext import commands
import discord
from sql import get_db
from discord.commands.context import ApplicationContext
from utils.constants import SUBMISSIONS_CHANNEL
from discord.mentions import AllowedMentions


class Submit(commands.Cog):
    CATEGORIES = [
        '60s: Hay', '60s: Wood', "60s: Carrots", "60s: Pumpkins", "60s: Power", "60s: Gold", "60s: Cactus", "60s: Bones",
        "Maze: 300", "Maze: 100", "Maze: 200 8x8", "Maze: 10x20"
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='submit', description="Submit a score")
    async def submit(self, ctx: ApplicationContext, category: discord.Option(str, choices=CATEGORIES), score: float, proof: discord.Attachment):
        """A submit command that submits a score.

        Args:
            ctx (commands.Context): The command context.
            category (str): The category to which the score belongs.
            score (int): The score being claimed.
            proof (discord.Attachment): A file containing the proof of the score.
        """
        submission_message = f"<@{ctx.user.id}> submitted a score of `{score}` in `{category}`. {proof.url}"
        response_message = f"Submitted a score of `{score}` in `{category}`.\nThe score will be added to the leaderboard after review.\nPlease be patient!"

        # AllowedMentions(users=False) allows us to mention the user but not ping them
        await ctx.bot.get_channel(SUBMISSIONS_CHANNEL).send(submission_message, allowed_mentions=AllowedMentions(users=False))
        await ctx.respond(response_message)


def setup(bot):
    bot.add_cog(Submit(bot))
