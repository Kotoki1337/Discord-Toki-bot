import calendar
import time
import json
import os
import disnake
from disnake.ext import commands

from discord_token import TOKEN

intents = disnake.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

timestamp = calendar.timegm(time.gmtime())

def check_if_it_is_me(ctx):
    return ctx.message.author.id == 276627005280092162

@bot.event
async def on_ready():
    await bot.change_presence(status = disnake.Status.dnd, activity = disnake.Game(name = f"为 {len(bot.guilds)} 个服务器提供色图"))

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py") and filename != "settings.py" and not (filename.startswith("__")):
        bot.load_extension(f"Cogs.{filename[:-3]}")

if __name__ == "__main__":
    bot.run(TOKEN)
