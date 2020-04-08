import discord
from discord.ext import commands
import json

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} leave..')

def setup(bot):
    bot.add_cog(Event(bot))