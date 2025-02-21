import discord
from discord.ext import commands
import traceback
import sys
from utils.logger import setup_logger

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger('cogs.events')

    # ===== General Bot Events =====
    @commands.Cog.listener()
    async def on_connect(self):
        self.logger.info("Bot connected to Discord")

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.logger.warning("Bot disconnected from Discord")

    @commands.Cog.listener()
    async def on_resumed(self):
        self.logger.info("Bot connection resumed")

    # ===== Guild Events =====
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.logger.info(f"Left guild: {guild.name} (ID: {guild.id})")

    # ===== Member Events =====
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.logger.info(f"Member joined: {member} (ID: {member.id}) to {member.guild.name}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        self.logger.info(f"Member left: {member} (ID: {member.id}) from {member.guild.name}")

    # ===== Message Events =====
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        # We don't log every message to avoid spam
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            self.logger.info(f"Bot mentioned by {message.author} in {message.guild.name if message.guild else 'DM'}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        self.logger.info(f"Message deleted in {message.guild.name if message.guild else 'DM'}, Channel: {message.channel.name if hasattr(message.channel, 'name') else 'N/A'}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.content != after.content:
            self.logger.info(f"Message edited in {before.guild.name if before.guild else 'DM'}, Channel: {before.channel.name if hasattr(before.channel, 'name') else 'N/A'}")

    # ===== Error Handling =====
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Skip errors that are already handled locally
        if hasattr(ctx.command, 'on_error'):
            return

        # Get the original error
        error = getattr(error, 'original', error)
        
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Command not found. Use `{ctx.prefix}help` to see available commands.")
            return
            
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'`{ctx.command}` is currently disabled.')
            return
            
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send(f'`{ctx.command}` cannot be used in Private Messages.')
            return
            
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: `{error.param.name}`. Use `{ctx.prefix}help {ctx.command}` for proper usage.")
            return
            
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid argument provided. Use `{ctx.prefix}help {ctx.command}` for proper usage.")
            return
        
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You lack the necessary permissions to run this command.")
            return
            
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"I lack the necessary permissions to execute this command.")
            return
            
        # For all other errors
        self.logger.error(f"Command error in {ctx.command}: {str(error)}")
        self.logger.error(''.join(traceback.format_exception(type(error), error, error.__traceback__)))
        
        # Inform the user
        error_message = f"An error occurred while executing the command `{ctx.command}`."
        if isinstance(error, Exception):
            error_message += f"\nError: {str(error)}"
        await ctx.send(error_message)

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        """Global error handler for all events"""
        self.logger.error(f"Error in event {event}")
        error_type, error_value, error_traceback = sys.exc_info()
        self.logger.error(''.join(traceback.format_exception(error_type, error_value, error_traceback)))

async def setup(bot):
    await bot.add_cog(Events(bot))