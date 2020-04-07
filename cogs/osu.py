import discord
from discord.ext import commands
import json
import urllib
import requests

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # bancho v2
    @commands.group(name="bancho", invoke_without_command=True)
    async def Osuppycommand(self, ctx):
        pass

    @Osuppycommand.command(name="user")
    async def user_subcommand(self, ctx, *, msg):
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

        embed=discord.Embed(title=username + "'s osu! Profile", url='https://osu.ppy.sh/users/' + uid)
        embed.set_author(name=username + "'s osu! Profile", url='https://osu.ppy.sh/users/' + uid,icon_url='https://osu.ppy.sh/images/flags/' + country + '.png')
        embed.add_field(name='Performance', value=pp, inline=True)
        embed.add_field(name='Rank', value='#' + pp_rank + '(' + country + '#' + pp_country_rank + ')', inline=True)
        embed.add_field(name='Accuracy', value=accuracy + '%', inline=True)
        embed.add_field(name='Play Count', value=pc, inline=True)
        await ctx.channel.send(embed=embed)

    # 国服 v1
    @commands.group(name="ppy.sb", invoke_without_command=True)
    async def Osusbcommand(self, ctx):
        await ctx.channel.send('WIP')

    @Osusbcommand.command(name="user")
    async def usersb_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/full?id={msg1}'
        else:
            url = f'https://osu.ppy.sb/api/v1/users/full?name={msg1}'
        r = requests.get(url)
        data = r.json()
        print(r.json())

        try:
            (m,) = msg2
        except ValueError:
            m = '0'

        if m == '0':
            mode = 'std'
        elif m == '1':
            mode = 'taiko'
        elif m == '2':
            mode = 'ctb'
        elif m == '3':
            mode = 'mania'
        else:
            mode = 'std'

        username = data['username']
        uid = data['id']
        country = data['country']
        pp = data[f'{mode}']['pp']
        pp_rank = data[f'{mode}']['global_leaderboard_rank']
        pp_country_rank = data[f'{mode}']['country_leaderboard_rank']
        accuracy = data[f'{mode}']['accuracy']
        pc = data[f'{mode}']['playcount']

        embed=discord.Embed(title=f"{username}'s {mode} stats", url=f'https://osu.ppy.sh/users/{uid}')
        embed.set_thumbnail(url=f'https://a.ppy.sb/{uid}')
        embed.set_author(name=f"{username}'s osu! Profile", url=f'https://osu.ppy.sh/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        embed.add_field(name='Performance', value=pp, inline=True)
        embed.add_field(name='Rank', value=f'#{pp_rank}({country}#{pp_country_rank})', inline=True)
        embed.add_field(name='Accuracy', value=f'{round(accuracy,2)}%', inline=True)
        embed.add_field(name='Play Count', value=pc, inline=True)
        await ctx.channel.send(embed=embed)

    @Osusbcommand.command(name="rx")
    async def userrxsb_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/rxfull?id={msg1}'
        else:
            url = f'https://osu.ppy.sb/api/v1/users/rxfull?name={msg1}'
        r = requests.get(url)
        data = r.json()
        print(r.json())

        try:
            (m,) = msg2
        except ValueError:
            m = '0'

        if m == '0':
            mode = 'std'
        elif m == '1':
            mode = 'taiko'
        elif m == '2':
            mode = 'ctb'
        elif m == '3':
            mode = 'mania'
        else:
            mode = 'std'

        username = data['username']
        uid = data['id']
        country = data['country']
        pp = data[f'{mode}']['pp']
        pp_rank = data[f'{mode}']['global_leaderboard_rank']
        pp_country_rank = data[f'{mode}']['country_leaderboard_rank']
        accuracy = data[f'{mode}']['accuracy']
        pc = data[f'{mode}']['playcount']

        embed=discord.Embed(title=f"{username}'s {mode} Relax stats", url=f'https://osu.ppy.sh/users/{uid}')
        embed.set_thumbnail(url=f'https://a.ppy.sb/{uid}')
        embed.set_author(name=f"{username}'s osu! Profile", url=f'https://osu.ppy.sh/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        embed.add_field(name='Performance', value=pp, inline=True)
        embed.add_field(name='Rank', value=f'#{pp_rank}({country}#{pp_country_rank})', inline=True)
        embed.add_field(name='Accuracy', value=f'{round(accuracy,2)}%', inline=True)
        embed.add_field(name='Play Count', value=pc, inline=True)
        await ctx.channel.send(embed=embed)

    @Osusbcommand.command(name="prrx")
    async def prrxsb_subcommand(self, ctx, msg1):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?id={msg1}'
        else:
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?name={msg1}'
        r = requests.get(url)
        data = r.json()
        print(r.json())

        m =  data['scores'][0]['play_mode']

        if m == 0:
            mode = 'std'
        elif m == 1:
            mode = 'taiko'
        elif m == 2:
            mode = 'ctb'

        max_combo = data['scores'][0]['beatmap']['max_combo']
        combo = data['scores'][0]['max_combo']
        n300 = data['scores'][0]['count_300']
        n100 = data['scores'][0]['count_100']
        n50 = data['scores'][0]['count_50']
        miss = data['scores'][0]['count_miss']
        song_name = data['scores'][0]['beatmap']['song_name']
        bid = data['scores'][0]['beatmap']['beatmap_id']
        set_bid = data['scores'][0]['beatmap']['beatmapset_id']
        current_pp = data['scores'][0]['pp']
        rank = data['scores'][0]['rank']


        embed=discord.Embed()
        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.ppy.sb/{msg1}')
        embed.add_field(name='300', value=f'x{n300}', inline=True)
        embed.add_field(name='100', value=f'x{n100}', inline=True)
        embed.add_field(name='50', value=f'x{n50}', inline=True)
        embed.add_field(name='Miss', value=f'x{miss}', inline=True)
        embed.add_field(name='Combo', value=f'{combo}/{max_combo}', inline=True)
        embed.add_field(name='Current PP', value=f'{current_pp}pp', inline=False)
        embed.add_field(name='Rank', value=f'{rank}', inline=False)
        embed.set_footer(text=f'Played on osu.ppy.sb with {mode} Relax')
        await ctx.channel.send(embed=embed)

    @Osusbcommand.command(name="pr")
    async def prsb_subcommand(self, ctx, msg1):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?id={msg1}'
        else:
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?name={msg1}'
        r = requests.get(url)
        data = r.json()
        print(r.json())

        m =  data['scores'][0]['play_mode']

        if m == 0:
            mode = 'std'
        elif m == 1:
            mode = 'taiko'
        elif m == 2:
            mode = 'ctb'
        elif m == 3:
            mode = 'mania'

        max_combo = data['scores'][0]['beatmap']['max_combo']
        combo = data['scores'][0]['max_combo']
        n300 = data['scores'][0]['count_300']
        n100 = data['scores'][0]['count_100']
        n50 = data['scores'][0]['count_50']
        miss = data['scores'][0]['count_miss']
        song_name = data['scores'][0]['beatmap']['song_name']
        bid = data['scores'][0]['beatmap']['beatmap_id']
        current_pp = data['scores'][0]['pp']
        rank = data['scores'][0]['rank']
        accuracy = data['scores'][0]['accuracy']


        embed=discord.Embed()
        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{bid}.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.ppy.sb/{msg1}')
        embed.add_field(name='300', value=f'x{n300}', inline=True)
        embed.add_field(name='100', value=f'x{n100}', inline=True)
        embed.add_field(name='50', value=f'x{n50}', inline=True)
        embed.add_field(name='Miss', value=f'x{miss}', inline=True)
        embed.add_field(name='Combo', value=f'{combo}/{max_combo}', inline=True)
        embed.add_field(name='accuracy', value=f'{accuracy}', inline=True)
        embed.add_field(name='Current PP', value=f'{current_pp}pp', inline=False)
        embed.add_field(name='Rank', value=f'{rank}', inline=False)
        embed.set_footer(text=f'Played on osu.ppy.sb with {mode}')
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Osu(bot))