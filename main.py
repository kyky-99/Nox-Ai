import os
import discord
import google.generativeai as genai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SYSTEM_PROMPT = """
Tum NOX AI ho.

Rules:
- Hamesha Hindi/Hinglish me reply do.
- Funny aur savage personality rakho.
- Agar koi gaali de to smart aur witty comeback do.
- Kabhi bhi offensive ya hateful mat banna.
- Short replies do (1-3 lines).
- Apne aap ko NOX AI bolo.
"""

@bot.event
async def on_ready():
    print(f"{bot.user} Online!")
    await bot.change_presence(activity=discord.Game("😈 Savage NOX AI"))

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        user_msg = message.content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip()

        if user_msg == "":
            user_msg = "Hello"

        try:
            response = model.generate_content(
                SYSTEM_PROMPT + "\nUser: " + user_msg
            )

            reply = response.text[:1900]

        except Exception:
            reply = "😅 Oye! Mera AI dimaag abhi thoda busy hai, thodi der baad try kar."

        await message.reply(reply)

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! NOX AI Online 😈")

bot.run(DISCORD_TOKEN)
