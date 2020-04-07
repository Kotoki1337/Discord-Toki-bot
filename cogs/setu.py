import discord
from discord.ext import commands
import json
import urllib
import requests

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Setu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="setu", invoke_without_command=True)
    async def Setucommand(self, ctx):
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
        await ctx.channel.send(embed=embed)

    @Setucommand.command(name="r18")
    async def r18_subcommand(self, ctx):
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

        if ctx.channel.is_nsfw():
            embed=discord.Embed(title=title, url=titleurl)
            embed.set_author(name=author, url=authorurl,icon_url=icon)
            embed.set_image(url=image)
            embed.add_field(name='R18', value=r18, inline=True)
            embed.add_field(name='Size', value=size, inline=True)
            embed.add_field(name='Tags', value=tags, inline=False)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f'当前不是`nsfw`频道。')

    @Setucommand.command(name="keyword")
    async def keyword_subcommand(self, ctx, msg):
        url = jdata['setukey_apikey'] + msg
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
        await ctx.channel.send(embed=embed)

    @Setucommand.command(name="mix")
    async def mix_subcommand(self, ctx):
        url = jdata['setumix_apikey']
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

        if r18 == False:
            embed=discord.Embed(title=title, url=titleurl)
            embed.set_author(name=author, url=authorurl,icon_url=icon)
            embed.set_image(url=image)
            embed.add_field(name='R18', value=r18, inline=True)
            embed.add_field(name='Size', value=size, inline=True)
            embed.add_field(name='Tags', value=tags, inline=False)
            await ctx.channel.send(embed=embed)
        else:
            if ctx.channel.is_nsfw():
                embed=discord.Embed(title=title, url=titleurl)
                embed.set_author(name=author, url=authorurl,icon_url=icon)
                embed.set_image(url=image)
                embed.add_field(name='R18', value=r18, inline=True)
                embed.add_field(name='Size', value=size, inline=True)
                embed.add_field(name='Tags', value=tags, inline=False)
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send(f'这张图片被标记为 `R18 限制级`，当前不是 `nsfw` 频道。')

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
    bot.add_cog(Setu(bot))