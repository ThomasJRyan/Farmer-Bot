import discord

from discord.ext import commands
from discord.commands.context import ApplicationContext

from sql.crud.faq import get_faq, add_faq, get_tags

from utils.constants import VERIFIER_ROLE

class FAQCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="faq", description="Frequently asked questions")
    async def get_faq(self: ApplicationContext, ctx, tag: discord.Option(
        str, description="Frequently asked question tag", autocomplete=get_tags)): # type: ignore
        """A command that displays a FAQ."""
        faq = await get_faq(tag)
        
        if not faq:
            await ctx.respond("No FAQ found with that tag.", ephemeral=True)
            return
        
        embed = discord.Embed(title=faq.question, description=faq.answer)
        await ctx.respond(embed=embed)
        
    @commands.slash_command(name="faq_add", description="Add an FAQ")
    @commands.has_any_role(VERIFIER_ROLE, "Bug Creator", "Mod")
    async def add_faq(self, ctx: ApplicationContext, tag: str, question: str, answer: str):
        """A command that adds a FAQ."""
        await add_faq(tag, question, answer)
        await ctx.respond("FAQ added.", ephemeral=True)
    
def setup(bot):
    bot.add_cog(FAQCog(bot))