import discord
from discord.ext import commands

import sys

sys.path.append("./core")
from classes import Cog_Extension

import json
import urllib
import requests

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Osu(Cog_Extension):

    @commands.group(name="osu", invoke_without_command=True)
    async def Osucommand(self, ctx):
        pass

    @Osucommand.command(name="user")
    async def user_subcommand(self, ctx, msg):
        url = 'https://osu.ppy.sh/api/get_user?k=' + jdata['osu_apikey'] + '&u=' + msg
        r = requests.get(url)
        data = r.json()
        print(r.json())

        username = data[0]['username']
        uid = data[0]['user_id']
        pp = data[0]['pp_raw']
        pp_rank = data[0]['pp_rank']
        pp_country_rank = data[0]['pp_country_rank']
        country = data[0]['country']
        accuracy = data[0]['accuracy']
        pc = data[0]['playcount']
        ranked_score = data[0]['ranked_score']

        embed=discord.Embed(title=username + "'s osu! Profile", url='https://osu.ppy.sh/users/' + uid)
        embed.set_author(name=username + "'s osu! Profile", url='https://osu.ppy.sh/users/' + uid,icon_url='https://osu.ppy.sh/images/flags/' + country + '.png' + country + ".png")
        embed.add_field(name='Performance', value=pp, inline=True)
        embed.add_field(name='Rank', value='#' + pp_rank + '(' + country + '#' + pp_country_rank + ')', inline=True)
        embed.add_field(name='Accuracy', value=accuracy + '%', inline=True)
        embed.add_field(name='Play Count', value=pc, inline=True)
        embed.add_field(name='Ranked score', value=ranked_score, inline=True)
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Osu(bot))