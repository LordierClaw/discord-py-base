import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX', '!')
GUILD_ID = os.getenv('GUILD_ID')  # For development/testing

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'bot.log'