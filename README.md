# Farmer Bot

This is a Discord bot that is designed to help with the "The Farmer Was Replaced" community. The bot is designed to be 
run in a Docker container and uses a MySQL database to store data. The bot is written in Python and uses the py-cord
library.

## Installation

1. Clone the repository
2. Create a `.env` file with the following content:
```
DISCORD_TOKEN=your_token_here
GUILD_ID=your_guild_id_here

# These are arbitrary values. You could leave them as is if you wanted
MYSQL_USER=your_mysql_user_here
MYSQL_DATABASE=your_mysql_database_here
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_ROOT_PASSWORD=your_mysql_root_password_here
```
3. Run `docker compose up` to start the bot and the MySQL database