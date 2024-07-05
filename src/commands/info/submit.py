from discord.ext import commands
import discord


class Submit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='submit', description="Submit a score")
    async def submit(self, ctx, category: discord.Option(str, choices=['60s: Hay', '60s: Wood']), score: float, proof: discord.Attachment):
        """A submit command that submits a score.

        Args:
            ctx (commands.Context): The command context.
            category (str): The category to which the score belongs.
            score (int): The score being claimed.
            proof (discord.Attachment): A file containing the proof of the score.
        """
        await ctx.respond(f"Submitting {category}!", ephemeral=True)


def setup(bot):
    bot.add_cog(Submit(bot))
