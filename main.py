import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    await bot.change_presence(activity=discord.Game("THE NOX AI 😈"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        await message.reply("😈 Kya hua? NOX AI ko mention kiya? Ab bol, kya kaam hai?")

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! NOX AI is online.")

bot.run(TOKEN)
