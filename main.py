import os
import discord
import google.generativeai as genai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN missing!")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing!")

if CHANNEL_ID == 0:
    raise ValueError("CHANNEL_ID missing!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SYSTEM_PROMPT = """
Tum NOX AI ho.

Rules:
- Hindi/Hinglish me baat karo.
- Funny aur savage personality rakho.
- Smart aur witty comeback do.
- Offensive ya hateful mat banna.
- Reply 1-3 lines me do.
"""

@bot.event
async def on_ready():
    print(f"{bot.user} Online!")
    await bot.change_presence(activity=discord.Game("😈 Savage NOX AI"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        await bot.process_commands(message)
        return

    try:
        response = model.generate_content(
            SYSTEM_PROMPT + "\nUser: " + message.content
        )

        reply = response.text[:1900]

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    await message.reply(reply)
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! NOX AI Online 😈")

bot.run(DISCORD_TOKEN, log_handler=None)
