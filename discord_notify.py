import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guilds')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="ping", description="Responds with pong")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f"An error occurred: {error}")

# Run the bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in environment variables")
        print("Please create a .env file with your Discord bot token:")
        print("DISCORD_TOKEN=your_bot_token_here")
        exit(1)
    
    bot.run(TOKEN)
