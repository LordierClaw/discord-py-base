import discord
from discord.ext import commands
import asyncio
import os
from config import TOKEN, PREFIX, GUILD_ID
from utils.logger import setup_logger

# Setup logger
logger = setup_logger('bot')

# Define intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize bot with command prefix and intents
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            intents=intents,
            help_command=None,  # Disable default help command
            case_insensitive=True
        )
        self.logger = logger
    
    async def setup_hook(self):
        # Load all cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    self.logger.info(f'Loaded extension: cogs.{filename[:-3]}')
                except Exception as e:
                    self.logger.error(f'Failed to load extension {filename}: {e}')
        
        # Sync commands with Discord
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            self.logger.info(f'Synced commands to guild {GUILD_ID}')
        else:
            await self.tree.sync()
            self.logger.info('Synced global commands')

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{PREFIX}help"
        )
        await self.change_presence(activity=activity)

async def main():
    bot = Bot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())