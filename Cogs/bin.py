from disnake.ext import commands
import urllib.parse
import aiohttp
import disnake
import json

from Cogs.settings import bin_url

imgDisc = {
    "visa" : "https://i.imgur.com/0hRwdTB.png",
    "mastercard" : "https://i.imgur.com/trcmNP1.png",
    "jcb" : "https://i.imgur.com/9hBVeLd.png",
    "unionpay" : "https://i.imgur.com/ontFgch.png",
    "maestro" : "https://i.imgur.com/3xL8Ydn.png",
    "discover" : "https://i.imgur.com/5xqEnhS.png",
    "amex" : "https://i.imgur.com/z3QcGKH.png"
}

class Bin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="查询银行卡 BIN 信息")
    async def bin(self, ctx, bin: int = commands.Param(description="Bin 头")):
        url = f"{bin_url}{bin}"
        async with aiohttp.ClientSession() as client:
            r = await client.get(url)
            try:
                data = await r.json()

                payment = data['scheme']
                try:
                    cardType = data['type'].title()
                except:
                    cardType = "Unknown"
                try:
                    brand = data['brand'].title()
                except:
                    brand = "Unknown"
                try:
                    countryEmoji = data['country']['emoji']
                except:
                    countryEmoji = ":earth_africa::earth_americas::earth_asia:"
                try:
                    countryName = data['country']['name']
                except:
                    countryName = "At least in earth"
                country = f"{countryEmoji}  {countryName}"
                try:
                    bankName = data['bank']['name']
                except:
                    bankName = "Unknown"
                try:
                    prepaid = data['prepaid']
                    if prepaid == True:
                        prepaid = "Yes"
                    else:
                        prepaid = "No"
                except:
                    prepaid = "Unknown"
                try:
                    bankUrl = data['bank']['url']
                except:
                    params = {'q': bankName}
                    bankUrl = f"www.google.com/search?{urllib.parse.urlencode(params)}"
                bankMarkdown = f"[{bankName}](http://{bankUrl})"
                imgnone = "https://i.imgur.com/T6zlZMD.png",
                img = imgDisc.get(payment, imgnone)

                if payment == "unionpay":
                    payment = "中国银联"
                else:
                    payment = payment.title()

                embed=disnake.Embed (
                    description=f"{payment} {country}"
                )
                embed.set_author(name=f"BIN {bin} available information", icon_url=img)
                embed.add_field(name='CARD INFORMATION', value=f"**Type**: {cardType}\n**Brand**: {brand}\n**Prepaid?**: {prepaid}\n", inline=False)
                embed.add_field(name='BANK INFORMATION', value=bankMarkdown, inline=False)
                await ctx.send(embed=embed)
            except:
                if bin == "":
                    embed=disnake.Embed (
                        description="Use **!bin {YOUR CARD BIN}** to check an bin available"
                    )
                    embed.set_author(name=f"BIN wiki help", icon_url="https://i.imgur.com/T6zlZMD.png")
                    await ctx.send(embed=embed)
                else:
                    embed=disnake.Embed (
                        description=f"Cannot find this BIN from API\nTry to use 6-8 digits"
                    )
                    embed.set_author(name=f"BIN {bin} unavailable", icon_url="https://i.imgur.com/T6zlZMD.png")
                    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Bin(bot))