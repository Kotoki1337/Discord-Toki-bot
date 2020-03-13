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

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} join!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(jdata['Notice_channel']))
        await channel.send(f'{member} 离开了伺服器。')


    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == '竹竹来张色图':
            url = jdata['setu_apikey']
            r = requests.get(url)
            print(r.json())
            data = r.json()

            icon = jdata['pic_pixiv']
            title = data['data'][0]['title']
            titleurl = 'https://www.pixiv.net/artworks/' + str(data['data'][0]['pid'])
            author = data['data'][0]['author']
            authorurl = 'https://www.pixiv.net/users/' + str(data['data'][0]['uid'])
            image = data['data'][0]['url']
            r18 = data['data'][0]['r18']
            size = str(data['data'][0]['width']) + 'x' + str(data['data'][0]['height'])
            tags = data['data'][0]['tags']

            embed=discord.Embed(title=title, url=titleurl)
            embed.set_author(name=author, url=authorurl,icon_url=icon)
            embed.set_image(url=image)  
            embed.add_field(name='R18', value=r18, inline=True)
            embed.add_field(name='Size', value=size, inline=True)
            embed.add_field(name='Tags', value=tags, inline=False)
            await msg.channel.send(embed=embed)  

        elif msg.content == '竹竹来张R18色图':
            url = jdata['setur18_apikey']
            r = requests.get(url)
            print(r.json())
            data = r.json()

            icon = jdata['pic_pixiv']
            title = data['data'][0]['title']
            titleurl = 'https://www.pixiv.net/artworks/' + str(data['data'][0]['pid'])
            author = data['data'][0]['author']
            authorurl = 'https://www.pixiv.net/users/' + str(data['data'][0]['uid'])
            image = data['data'][0]['url']
            r18 = data['data'][0]['r18']
            size = str(data['data'][0]['width']) + 'x' + str(data['data'][0]['height'])
            tags = data['data'][0]['tags']

            if msg.channel.is_nsfw():
                embed=discord.Embed(title=title, url=titleurl)
                embed.set_author(name=author, url=authorurl,icon_url=icon)
                embed.set_image(url=image)  
                embed.add_field(name='R18', value=r18, inline=True)
                embed.add_field(name='Size', value=size, inline=True)
                embed.add_field(name='Tags', value=tags, inline=False)
                await msg.channel.send(embed=embed)
            else:
                await msg.channel.send(f'当前不是`nsfw`频道。')
def setup(bot):
    bot.add_cog(Event(bot))