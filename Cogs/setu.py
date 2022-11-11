from Cogs.console import Console
from disnake.ext import commands
import datetime
import disnake
import aiohttp
import json
import re

from Cogs.settings import pic_pixiv, setu_apikey

class Setu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        # https://github.com/Tsuk1ko/cq-picsearcher-bot/blob/b80d9b3810d22e8f5ca374ed91e2fd4d69d65c47/config.default.jsonc#L145
        setu = re.compile(r"[来來发發给給][张張个個幅点點份丶]{1}?(?P<r18>[Rr]18的?)?(?P<keyword>.*?)?的?[色瑟][图圖]|^--setu$").search(msg.content)

        if setu:
            await msg.channel.send(f'**注意：Discord 将在 2022 年 10 月 1 日后永久关闭消息内容特权意图，竹竹将无法继续从普通讯息中读取指令。请使用 Slash 命令 `/setu` 进行替代。**')

            keyword = setu.group("keyword") if setu.group("keyword") else ""
            r18 = 1 if setu.group("r18") else 0
            url = f"{setu_apikey}?r18={r18}&keyword={keyword}"
        else:
            return

        # console start
        print(f'{datetime.datetime.now().strftime("%x - [%X]")}\n    Command: {msg.content}\n    Sender:  {msg.author}\n    Guild:   {msg.guild}\n')
        # console end

        async with aiohttp.ClientSession() as client:
            r = await client.get(url)
            data = await r.json(content_type="application/json")

        if data["data"]:
            icon = pic_pixiv
            title = data['data'][0]['title']
            titleurl = 'https://www.pixiv.net/artworks/' + str(data['data'][0]['pid'])
            author = data['data'][0]['author']
            authorurl = 'https://www.pixiv.net/users/' + str(data['data'][0]['uid'])
            image = data['data'][0]['urls']["original"]
            r18 = data['data'][0]['r18']
            size = str(data['data'][0]['width']) + 'x' + str(data['data'][0]['height'])
            tagsList = data['data'][0]['tags']

            if keyword != "":
                tags = ", ".join(tagsList).replace(f"{keyword}", f"``{keyword}``").replace("r18", "").replace("R18", "")
            else:
                tags = ", ".join(tagsList)

            embed=disnake.Embed(title=title, url=titleurl)
            embed.set_author(name=author, url=authorurl,icon_url=icon)
            embed.set_image(url=image)
            embed.add_field(name='R18', value=r18, inline=True)
            embed.add_field(name='Size', value=size, inline=True)
            embed.add_field(name='Tags', value=tags, inline=False)
            embed.set_footer(text="Powerd by api.lolicon.app")

            if r18 == 0:
                await msg.channel.send(embed=embed)
            else:
                if msg.channel.is_nsfw():
                    await msg.channel.send(embed=embed)
                else:
                    await msg.channel.send(f'你请求的这张图片被标记为 `R18 限制级`，当前不是 `nsfw` 频道。')
        else:
            if keyword == "":
                await msg.channel.send(f"错误：API 返回了空值")
            else:
                await msg.channel.send(f"错误：API 返回了空值，你请求的关键字为 **{keyword}**，可能没有找到相关图片")

    @commands.slash_command(description="向竹竹请求一张色图")
    async def setu(
        self,
        ctx,
        keyword: str = commands.Param(description="关键词", default=""),
        r18: int = commands.Param(description="是否 R18", default=0, choices={"False": 0, "True": 1})
        ):

            if keyword != "":
                url = f"{setu_apikey}?r18={r18}&keyword={keyword}"
            else:
                url = setu_apikey

            async with aiohttp.ClientSession() as client:
                r = await client.get(url)
                data = await r.json(content_type="application/json")

            if data["data"]:
                icon = pic_pixiv
                title = data['data'][0]['title']
                titleurl = 'https://www.pixiv.net/artworks/' + str(data['data'][0]['pid'])
                author = data['data'][0]['author']
                authorurl = 'https://www.pixiv.net/users/' + str(data['data'][0]['uid'])
                image = data['data'][0]['urls']["original"]
                r18 = data['data'][0]['r18']
                size = str(data['data'][0]['width']) + 'x' + str(data['data'][0]['height'])
                tagsList = data['data'][0]['tags']

                if keyword != "":
                    tags = ", ".join(tagsList).replace(f"{keyword}", f"``{keyword}``").replace("r18", "").replace("R18", "")
                else:
                    tags = ", ".join(tagsList)

                embed=disnake.Embed(title=title, url=titleurl)
                embed.set_author(name=author, url=authorurl,icon_url=icon)
                embed.set_image(url=image)
                embed.add_field(name='R18', value=r18, inline=True)
                embed.add_field(name='Size', value=size, inline=True)
                embed.add_field(name='Tags', value=tags, inline=False)
                embed.set_footer(text="Powerd by api.lolicon.app")

                if r18 == 0:
                    await ctx.send(embed=embed)
                else:
                    if ctx.channel.is_nsfw():
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f'你请求的这张图片被标记为 `R18 限制级`，当前不是 `nsfw` 频道。')
            else:
                if keyword == "":
                    await ctx.send(f"错误：API 返回了空值")
                else:
                    await ctx.send(f"错误：API 返回了空值，你请求的关键字为 **{keyword}**，可能没有找到相关图片")

def setup(bot):
    bot.add_cog(Setu(bot))