from disnake.ext import commands
import disnake


from Models.tool import hash
from Models.maimaidx_music import *
from Models.image import *
from Models.maimai_best_40 import generate

import base64


class MaimaiDX(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(description="通过查分器查询舞萌 DX（中国大陆官方服务器）的 Best 40 成绩")
    async def b40(self, ctx, user: str = commands.Param(description="用户名")):
        if user != "":
            username = user
            # if username == "":
            #     payload = {'qq': str(event.get_user_id())}
            # else:
            payload = {'username': username}
            img, success = await generate(payload)
            if success == 400:
                await ctx.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。")
            elif success == 403:
                await ctx.send("该用户禁止了其他人获取数据。")
            else:
                imgstring = f"{str(image_to_base64(img), encoding='utf-8')}"
                imgdata = base64.b64decode(imgstring)
                with open("Static/b40.png", "wb") as fh:
                    fh.write(imgdata)
                await ctx.send(file=disnake.File("Static/b40.png"))
        else:
            await ctx.send("请使用 `user` 参数传入玩家名称。")


def setup(bot):
    bot.add_cog(MaimaiDX(bot))