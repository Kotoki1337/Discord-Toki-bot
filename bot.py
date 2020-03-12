import json
import os

import discord
from discord.ext import commands

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='[')

@bot.event
async def on_ready():
    print(">> Testing: This Bot is online <<")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'已加载 {extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'已卸载 {extension}')

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'已重载 {extension}')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

if __name__ == "__main__":
    bot.run(jdata['TOKEN'])
