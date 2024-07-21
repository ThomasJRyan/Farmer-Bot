import os

BOT_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

SUBMISSIONS_CHANNEL = int(os.getenv('SUBMISSIONS_CHANNEL'))
VERIFIER_ROLE = int(os.getenv('VERIFIER_ROLE', 0))