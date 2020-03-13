import discord
from discord.ext import commands
import sys

sys.path.append("./core")
from classes import Cog_Extension

class Main(Cog_Extension):

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

def setup(bot):
    bot.add_cog(Main(bot))
