from disnake.ext import commands
import disnake
import requests
import json

from Cogs.settings import pic_nmsl

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Bot 还活着吗")
    async def ping(self, ctx):
        r = requests.get("http://ip-api.com/json/")
        data = r.json()
        country = data['country']
        # regionName = data['regionName']
        city = data['city']
        isp = data['isp']

        await ctx.send(f'**{round(self.bot.latency*1000)}** ms on **{country}** server by **{isp}** in **{city}**')

    # @commands.slash_command()
    # async def help(self, ctx):
    #     embed=disnake.Embed(title="帮助")
    #     embed.add_field(name="命令列表", value="竹竹来张色图\n\nThat's All\n\n想知道更多？\n[Github Repo](https://github.com/Kotoki1337/Discord-Toki-Bot)\n[Discord Support Server](https://discord.gg/v92vWwQBY5)", inline=True)
    #     await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Main(bot))
