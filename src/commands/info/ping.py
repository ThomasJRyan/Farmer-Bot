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
        
    @commands.slash_command(name='pong', description="Replies with Ping!")
    async def pong(self, ctx):
        """A pong command that replies with Ping!

        Args:
            ctx (commands.Context): The command context.
        """
        await ctx.respond("Ping!")


def setup(bot):
    bot.add_cog(Ping(bot))
