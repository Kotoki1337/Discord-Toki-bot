import discord
from discord.ext import commands

import sys

sys.path.append("./core")
from classes import Cog_Extension

import json

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class React(Cog_Extension):

    @commands.command()
    async def nmsl(self, ctx):
        pic = discord.File(jdata['pic_nmsl'])
        await ctx.send(file= pic)

def setup(bot):
    bot.add_cog(React(bot))
