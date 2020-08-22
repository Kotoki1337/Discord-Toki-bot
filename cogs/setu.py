from discord.ext import commands
import discord
import aiohttp
import json
import re

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Setu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == '竹竹来张色图':
            url = jdata['setumix_apikey']

            async with aiohttp.ClientSession() as client:
                r = await client.get(url)
                data = await r.json()

            icon = jdata['pic_pixiv']
            title = data['data'][0]['title']
            titleurl = 'https://www.pixiv.net/artworks/' + str(data['data'][0]['pid'])
            author = data['data'][0]['author']
            authorurl = 'https://www.pixiv.net/users/' + str(data['data'][0]['uid'])
            image = data['data'][0]['url']
            r18 = data['data'][0]['r18']
            size = str(data['data'][0]['width']) + 'x' + str(data['data'][0]['height'])
            tags = data['data'][0]['tags']

            if r18 == False:
                embed=discord.Embed(title=title, url=titleurl)
                embed.set_author(name=author, url=authorurl,icon_url=icon)
                embed.set_image(url=image)
                embed.add_field(name='R18', value=r18, inline=True)
                embed.add_field(name='Size', value=size, inline=True)
                embed.add_field(name='Tags', value=tags, inline=False)
                await msg.channel.send(embed=embed)
            else:
                if msg.channel.is_nsfw():
                    embed=discord.Embed(title=title, url=titleurl)
                    embed.set_author(name=author, url=authorurl,icon_url=icon)
                    embed.set_image(url=image)
                    embed.add_field(name='R18', value=r18, inline=True)
                    embed.add_field(name='Size', value=size, inline=True)
                    embed.add_field(name='Tags', value=tags, inline=False)
                    await msg.channel.send(embed=embed)
                else:
                    await msg.channel.send(f'这张图片被标记为 `R18 限制级`，当前不是 `nsfw` 频道。')

        elif msg.content == '竹竹来张R18色图':
            url = jdata['setur18_apikey']

            async with aiohttp.ClientSession() as client:
                r = await client.get(url)
                data = await r.json()

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
        else:
            res = re.search("竹竹来张(.+)色图", str(msg.content))
            if res is not None:
                keyword = res.group(1)
                if "R18" in keyword or "r18" in keyword:
                    url = jdata['setukey_apikey_R18'] + keyword.replace("R18", "").replace("r18", "")
                else:
                    url = jdata['setukey_apikey'] + keyword

                async with aiohttp.ClientSession() as client:
                    r = await client.get(url)
                    data = await r.json()

                icon = jdata['pic_pixiv']
                title = data['data'][0]['title']
                titleurl = 'https://www.pixiv.net/artworks/' + str(data['data'][0]['pid'])
                author = data['data'][0]['author']
                authorurl = 'https://www.pixiv.net/users/' + str(data['data'][0]['uid'])
                image = data['data'][0]['url']
                r18 = data['data'][0]['r18']
                size = str(data['data'][0]['width']) + 'x' + str(data['data'][0]['height'])
                tags = data['data'][0]['tags']

                if r18 == False:
                    embed=discord.Embed(title=title, url=titleurl)
                    embed.set_author(name=author, url=authorurl,icon_url=icon)
                    embed.set_image(url=image)
                    embed.add_field(name='R18', value=r18, inline=True)
                    embed.add_field(name='Size', value=size, inline=True)
                    embed.add_field(name='Tags', value=tags, inline=False)
                    await msg.channel.send(embed=embed)
                else:
                    if msg.channel.is_nsfw():
                        embed=discord.Embed(title=title, url=titleurl)
                        embed.set_author(name=author, url=authorurl,icon_url=icon)
                        embed.set_image(url=image)
                        embed.add_field(name='R18', value=r18, inline=True)
                        embed.add_field(name='Size', value=size, inline=True)
                        embed.add_field(name='Tags', value=tags, inline=False)
                        await msg.channel.send(embed=embed)
                    else:
                        await msg.channel.send(f'这张图片被标记为 `R18 限制级`，当前不是 `nsfw` 频道。')
            else:
                pass

def setup(bot):
    bot.add_cog(Setu(bot))