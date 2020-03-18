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

class Corona(Cog_Extension):

    @commands.group(name="corona", invoke_without_command=True)
    async def Coronacommand(self, ctx):
        url = 'https://corona.lmao.ninja/all'
        r = requests.get(url)
        data = r.json()
        print(r.json())

        cases = data['cases']
        deaths = data['deaths']
        recovered = data['recovered']

        embed=discord.Embed(title='Overall')
        embed.set_author(name='COVID-19 CORONAVIRUS OUTBREAK', url='https://www.worldometers.info/coronavirus/')
        embed.add_field(name='Total cases', value=cases, inline=True)
        embed.add_field(name='Total deaths', value=deaths, inline=True)
        embed.add_field(name='Total recovered', value=recovered, inline=False)
        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Corona(bot))


    