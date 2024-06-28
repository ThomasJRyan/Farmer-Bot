# Discord Bot Template

This is a template for a Discord bot written in Python. It uses the py-cord library.

## Installation

1. Clone the repository
2. Create a `.env` file with the following content:
```
DISCORD_TOKEN=your_token_here
GUILD_ID=your_guild_id_here

MYSQL_ROOT_PASSWORD=your_mysql_root_password_here
MYSQL_DATABASE=your_mysql_database_here
MYSQL_USER=your_mysql_user_here
MYSQL_PASSWORD=your_mysql_password_here
```
3. Run `docker compose up` to start the bot and the MySQL database

## Development

The bot is written in Python and uses the py-cord library. The bot is split into several modules, each of which is 
responsible for a specific feature. The modules are loaded dynamically when the bot starts. The bot mounts a volume to
to the `src` directory, so you can make changes to the bot without having to restart the container. The cogwatch 
module will automatically reload the cogs when they are changed.
