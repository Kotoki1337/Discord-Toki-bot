from discord.ext import commands
import urllib.parse
import aiohttp
import discord
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

    @commands.command()
    async def bin(self, ctx, msg=""):
        url = f"{bin_url}{msg}"
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

                embed=discord.Embed (
                    description=f"{payment} {country}"
                )
                embed.set_author(name=f"BIN {msg} available information", icon_url=img)
                embed.add_field(name='CARD INFORMATION', value=f"**Type**: {cardType}\n**Brand**: {brand}\n**Prepaid?**: {prepaid}\n", inline=False)
                embed.add_field(name='BANK INFORMATION', value=bankMarkdown, inline=False)
                await ctx.channel.send(embed=embed)
            except:
                if msg == "":
                    embed=discord.Embed (
                        description="Use **!bin {YOUR CARD BIN}** to check an bin available"
                    )
                    embed.set_author(name=f"BIN wiki help", icon_url="https://i.imgur.com/T6zlZMD.png")
                    await ctx.channel.send(embed=embed)
                else:
                    embed=discord.Embed (
                        description=f"Cannot find this BIN from API\nTry to use 6-8 digits"
                    )
                    embed.set_author(name=f"BIN {msg} unavailable", icon_url="https://i.imgur.com/T6zlZMD.png")
                    await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Bin(bot))