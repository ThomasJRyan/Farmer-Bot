from discord import guild_only
from discord.ext import commands


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='user', description="Provides information about the user.")
    @guild_only()
    async def user(self, ctx):
        """Provides information about the user.
        May only be used in a guild.

        Args:
            ctx (commands.Context): The command context.
        """
        await ctx.respond(
            f"This command was run by {ctx.author.display_name}, "
            f"who joined on {ctx.author.joined_at.strftime('%A, %B %d %Y @ %H:%M:%S %p')}"
        )


def setup(bot):
    bot.add_cog(User(bot))
