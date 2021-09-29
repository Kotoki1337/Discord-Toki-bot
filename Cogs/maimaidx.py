from discord.ext import commands
import discord


from Models.tool import hash
from Models.maimaidx_music import *
from Models.image import *
from Models.maimai_best_40 import generate

import base64


class MaimaiDX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def b40(self, ctx, args=""):
        if args != "":
            username = args
            # if username == "":
            #     payload = {'qq': str(event.get_user_id())}
            # else:
            payload = {'username': username}
            img, success = await generate(payload)
            if success == 400:
                await ctx.channel.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。")
            elif success == 403:
                await ctx.channel.send("该用户禁止了其他人获取数据。")
            else:
                imgstring = f"{str(image_to_base64(img), encoding='utf-8')}"
                imgdata = base64.b64decode(imgstring)
                with open("Static/b40.png", "wb") as fh:
                    fh.write(imgdata)
                await ctx.send(file=discord.File("Static/b40.png"))


def setup(bot):
    bot.add_cog(MaimaiDX(bot))