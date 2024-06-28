from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='ping', description="Replies with Pong!")
    async def ping(self, ctx):
        """A ping command that replies with Pong!

        Args:
            ctx (commands.Context): The command context.
        """
        await ctx.respond("Pong!")


def setup(bot):
    bot.add_cog(Ping(bot))
