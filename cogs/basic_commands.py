import discord
from discord import app_commands
from discord.ext import commands
import time
from utils.logger import setup_logger

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger('cogs.basic')

    # ===== Regular commands =====
    @commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx):
        """Check the bot's latency"""
        start_time = time.time()
        message = await ctx.send("Pinging...")
        end_time = time.time()
        
        latency = round(self.bot.latency * 1000)
        api_latency = round((end_time - start_time) * 1000)
        
        embed = discord.Embed(title="Pong! 🏓", color=discord.Color.green())
        embed.add_field(name="Bot Latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="API Latency", value=f"{api_latency}ms", inline=True)
        
        self.logger.info(f"Ping command used by {ctx.author} - Latency: {latency}ms")
        await message.edit(content=None, embed=embed)

    @commands.command(name="help", description="Shows the help menu")
    async def help_command(self, ctx, command_name=None):
        """Shows information about commands"""
        if command_name:
            # Get specific command help
            command = self.bot.get_command(command_name)
            if not command:
                await ctx.send(f"Command `{command_name}` not found.")
                return
                
            embed = discord.Embed(
                title=f"Help: {command.name}",
                description=command.help or "No description available.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Usage", value=f"`{ctx.prefix}{command.name} {command.signature}`")
            self.logger.info(f"Help command used by {ctx.author} for command: {command_name}")
            
        else:
            # General help menu
            embed = discord.Embed(
                title="Bot Help Menu",
                description=f"Use `{ctx.prefix}help <command>` for more information on a command.",
                color=discord.Color.blue()
            )
            
            # Group commands by cog
            for cog_name, cog in self.bot.cogs.items():
                commands_list = cog.get_commands()
                if commands_list:
                    command_texts = []
                    for cmd in commands_list:
                        command_texts.append(f"`{cmd.name}` - {cmd.help or 'No description'}")
                    
                    embed.add_field(
                        name=cog_name,
                        value="\n".join(command_texts),
                        inline=False
                    )
            
            # Add slash command section
            embed.add_field(
                name="Slash Commands",
                value="Type `/` to see available slash commands.",
                inline=False
            )
            
            self.logger.info(f"Help command (general) used by {ctx.author}")
            
        await ctx.send(embed=embed)

    # ===== Slash commands =====
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def slash_ping(self, interaction: discord.Interaction):
        start_time = time.time()
        await interaction.response.defer()
        end_time = time.time()
        
        latency = round(self.bot.latency * 1000)
        api_latency = round((end_time - start_time) * 1000)
        
        embed = discord.Embed(title="Pong! 🏓", color=discord.Color.green())
        embed.add_field(name="Bot Latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="API Latency", value=f"{api_latency}ms", inline=True)
        
        self.logger.info(f"Slash ping command used by {interaction.user} - Latency: {latency}ms")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="help", description="Shows the help menu")
    async def slash_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Bot Help Menu",
            description="Below are the available commands:",
            color=discord.Color.blue()
        )
        
        # List regular commands
        regular_cmds = []
        for command in self.bot.commands:
            if not command.hidden:
                regular_cmds.append(f"`{command.name}` - {command.help or 'No description'}")
        
        # List slash commands
        slash_cmds = []
        for command in self.bot.tree.walk_commands():
            slash_cmds.append(f"`/{command.name}` - {command.description}")
        
        embed.add_field(name="Regular Commands", value="\n".join(regular_cmds) or "No commands available", inline=False)
        embed.add_field(name="Slash Commands", value="\n".join(slash_cmds) or "No commands available", inline=False)
        
        self.logger.info(f"Slash help command used by {interaction.user}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))