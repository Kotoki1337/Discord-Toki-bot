import discord
from discord.ext import commands
import json
import requests

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        r = requests.get("http://ip-api.com/json/")
        data = r.json()
        country = data['country']
        # regionName = data['regionName']
        city = data['city']
        isp = data['isp']

        await ctx.send(f'**{round(self.bot.latency*1000)}** ms on **{country}** server by **{isp}** in **{city}**')

    @commands.command()
    async def nmsl(self, ctx):
        pic = discord.File(jdata['pic_nmsl'])
        await ctx.send(file= pic)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(f'**No help here now**')

def setup(bot):
    bot.add_cog(Main(bot))
