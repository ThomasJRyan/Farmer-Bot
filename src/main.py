"""Main file for the bot."""
import os
import asyncio

import discord

from cogwatch import Watcher
from discord.ext import commands

from utils.constants import BOT_TOKEN, GUILD_ID

INTENTS = discord.Intents.default()
INTENTS.message_content = True

SETTINGS = {
    "command_prefix": "!",
    "intents": INTENTS,
    "debug_guilds": [GUILD_ID],
}


class FarmerBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        """Prints a message when the bot is ready. Additionally, loads all cogs."""
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        """Processes commands when a message is sent. Additionally, ignores bots.

        Args:
            message (discord.Message): The message that was sent.
        """
        if message.author.bot:
            return

        await self.process_commands(message)

    async def start(self, *args, **kwargs):
        """Starts the bot. Passing in the token"""
        return await super().start(BOT_TOKEN, *args, **kwargs)

async def main(loop):
    """Starts the bot."""
    bot = FarmerBot(**SETTINGS)
    
    commands_watcher = Watcher(bot, 'commands', preload=True, debug=False)
    await commands_watcher.start()
    
    await bot.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
