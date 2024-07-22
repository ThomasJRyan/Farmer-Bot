import re
import discord

from discord.ext import commands
from discord.mentions import AllowedMentions
from discord.commands.context import ApplicationContext

from sql import get_db, get_engine
from sql.models.leaderboard import LeaderboardCategory, LeaderboardScore, get_categories
from utils.constants import SUBMISSIONS_CHANNEL, VERIFIER_ROLE

class Submit(commands.Cog):
    SUBMISSION_REGEX = re.compile(r"^<@(?P<user_id>\d+)>.*`(?P<score>.*)`.*`(?P<category>.*)`\. (?P<url>.*)$")

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='submit', description="Submit a score")
    async def submit(self, ctx: ApplicationContext, category: discord.Option(str, autocomplete=get_categories), score: float, proof: discord.Attachment):
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
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """A listener that listens for messages in the submissions channel.
        Will add reactions to the message if it's a bot message and ignore
        all other messages.

        Args:
            message (discord.Message): The message object.
        """
        # If the message isn't from us or the message is not in the submissions channel, return
        if not message.author.bot or message.channel.id != SUBMISSIONS_CHANNEL:
            return
        
        # If the message doesn't match the submission regex, return
        submission = self.SUBMISSION_REGEX.match(message.content)
        if not submission:
            return
        
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """A listener that listens for reactions added to messages in the submissions channel.
        Removes the reaction added by the bot once a reaction is added.

        Args:
            reaction (discord.Reaction): The reaction object.
            user (discord.User): The user who added the reaction.
        """
        # If the user is a bot or the message is not in the submissions channel, return
        if user.bot or reaction.message.channel.id != SUBMISSIONS_CHANNEL:
            return
        
        # If the message doesn't match the submission regex, return
        submission = self.SUBMISSION_REGEX.match(reaction.message.content)
        if not submission:
            return
        group = submission.groupdict()
        
        print(group['user_id'], group['score'], group['category'], group['url'])
        print(self.bot.get_user(int(group['user_id'])))
        print(reaction.message.channel.guild.get_member(int(group['user_id'])))
        
        # If the user doesn't have the verifier role, remove the reaction
        # If the verifier role is not set, then anyone can verify the score
        if VERIFIER_ROLE and VERIFIER_ROLE not in [role.id for role in user.roles]:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return
        
        if reaction.emoji == "✅":
            # Add the score to the database
            with get_db() as db:
                category = db.query(LeaderboardCategory).filter(LeaderboardCategory.category_name == group['category']).first()
                score = LeaderboardScore(msg_id=reaction.message.id, user_id=group['user_id'], score=group['score'], url=group['url'], category_id=category.category_id)
                db.add(score)
                db.commit()
        elif reaction.emoji == "❌":
            pass
        else:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return
        
        await reaction.message.remove_reaction("✅", self.bot.user)
        await reaction.message.remove_reaction("❌", self.bot.user)




def setup(bot):
    bot.add_cog(Submit(bot))
