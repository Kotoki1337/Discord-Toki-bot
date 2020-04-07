import discord
from discord.ext import commands
import json
import urllib
import requests

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 国服 v1
    @commands.group(name="test", invoke_without_command=True)
    async def Testsbcommand(self, ctx):
        await ctx.channel.send('WIP')

    @Testsbcommand.command(name="prrx")
    async def Testxsb_subcommand(self, ctx, msg1):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?id={msg1}'
        else:
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?name={msg1}'
        r = requests.get(url)
        data = r.json()
        print(r.json())

        m =  data['scores'][0]['beatmap']['play_mode']

        print(m)
        print(type(m))
        print(int(m))

def setup(bot):
    bot.add_cog(Test(bot))