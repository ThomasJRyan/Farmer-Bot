from discord import guild_only
from discord.ext import commands


class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='server', description="Provides information about the server.")
    @guild_only()
    async def server(self, ctx):
        """Provides information about the server.
        May only be used in a guild.

        Args:
            ctx (commands.Context): The command context.
        """
        await ctx.respond(
            f"This server is {ctx.guild.name}, "
            f"and has {ctx.guild.member_count} members."
        )


def setup(bot):
    bot.add_cog(Server(bot))
