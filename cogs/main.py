import discord
from discord.ext import commands
import json


with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    @commands.command()
    async def nmsl(self, ctx):
        pic = discord.File(jdata['pic_nmsl'])
        await ctx.send(file= pic)

def setup(bot):
    bot.add_cog(Main(bot))
