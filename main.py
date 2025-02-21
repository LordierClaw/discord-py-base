import discord
from discord.ext import commands
import asyncio
import os
import importlib.util
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
        # Load all cogs from their subfolders
        cogs_dir = './cogs'
        for cog_category in os.listdir(cogs_dir):
            category_path = os.path.join(cogs_dir, cog_category)
            
            # Skip __init__.py and non-directories
            if not os.path.isdir(category_path) or cog_category.startswith('_'):
                continue
                
            # Look for cog modules in each subfolder
            for filename in os.listdir(category_path):
                if filename.endswith('.py') and not filename.startswith('_'):
                    cog_path = f'cogs.{cog_category}.{filename[:-3]}'
                    
                    # Check if this is a valid cog module (has setup function)
                    module_path = os.path.join(category_path, filename)
                    spec = importlib.util.spec_from_file_location(cog_path, module_path)
                    if spec is None:
                        continue
                        
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    if hasattr(module, 'setup'):
                        try:
                            await self.load_extension(cog_path)
                            self.logger.info(f'Loaded extension: {cog_path}')
                        except Exception as e:
                            self.logger.error(f'Failed to load extension {cog_path}: {e}')
        
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