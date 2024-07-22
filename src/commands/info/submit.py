import re
import discord

from discord.ext import commands
from discord.mentions import AllowedMentions
from discord.commands.context import ApplicationContext
from discord.ui.item import Item

from sql import get_db
from utils.constants import SUBMISSIONS_CHANNEL, VERIFIER_ROLE


class ApprovalButtons(discord.ui.View):
    def __init__(self, user: discord.User, score: float, category: str):
        super().__init__()
        self.user = user
        self.score = score
        self.category = category

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji="✅")
    async def approve_callback(self, button: discord.Button, interaction: discord.Interaction):
        # Checking if the user has the verifier role
        if VERIFIER_ROLE and VERIFIER_ROLE not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("you don't have permission to do that", ephemeral=True)
            return 
        
        # Disable the buttons.
        self.disable_all_items()
        await interaction.message.edit(view=self)

        #TODO: Add logic to handle adding the score to the database
        await interaction.response.send_message(
            f"<@{interaction.user.id}> approved score `{self.score}` for <@{self.user.id}> in category `{self.category}`",
            allowed_mentions=AllowedMentions(users=False)
        )
    
    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji="❌")
    async def reject_callback(self, button: discord.Button, interaction: discord.Interaction):
        # Checking if the user has the verifier role
        if VERIFIER_ROLE and VERIFIER_ROLE not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("you don't have permission to do that", ephemeral=True)
            return 
        
        # Disable the buttons.
        self.disable_all_items()
        await interaction.message.edit(view=self)

        # no database interaction is needed in case of rejection
        await interaction.response.send_message(
            f"<@{interaction.user.id}> rejected score `{self.score}` for <@{self.user.id}> in category `{self.category}`",
            allowed_mentions=AllowedMentions(users=False)
        )
        

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
        await ctx.bot.get_channel(SUBMISSIONS_CHANNEL).send(
            submission_message,
            allowed_mentions=AllowedMentions(users=False),
            view=ApprovalButtons(ctx.user, score, category)
        )
        await ctx.respond(response_message)


def setup(bot):
    bot.add_cog(Submit(bot))
