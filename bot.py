import calendar
import time
import json
import os
import discord
from discord.ext import commands

from discord_token import TOKEN

bot = commands.Bot(command_prefix="!", help_command = None)
timestamp = calendar.timegm(time.gmtime())

def check_if_it_is_me(ctx):
    return ctx.message.author.id == 276627005280092162

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.dnd, activity = discord.Game(name = f""))

@bot.command()
@commands.check(check_if_it_is_me)
async def load(ctx, extension):
    bot.load_extension(f"Cogs.{extension}")
    await ctx.send(f"已加载 {extension}")

@bot.command()
@commands.check(check_if_it_is_me)
async def unload(ctx, extension):
    bot.unload_extension(f"Cogs.{extension}")
    await ctx.send(f"已卸载 {extension}")

@bot.command()
@commands.check(check_if_it_is_me)
async def reload(ctx, extension):
    bot.reload_extension(f"Cogs.{extension}")
    await ctx.send(f"已重载 {extension}")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py") and filename != "settings.py" and not (filename.startswith("__")):
        bot.load_extension(f"Cogs.{filename[:-3]}")

if __name__ == "__main__":
    bot.run(TOKEN)
