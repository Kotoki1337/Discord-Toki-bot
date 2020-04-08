import discord
from discord.ext import commands
import json
import requests

with open('setting.json', mode='r', encoding='u8') as jfile:
    jdata = json.load(jfile)

# 格式化每三位+一个逗号
def parse_int(num):
    to_str=str(num) #转换成字符串
    count=0 #循环计数
    sumstr='' #待拼接的字符串
    for one_str in to_str[::-1]: #注意循环是倒着输出的
        count += 1 #计数
        if count %3==0 and count != len(to_str): #如果count等于3或3的倍数并且不等于总长度
            one_str = ',' + one_str # 当前循环的字符串前面加逗号
            sumstr = one_str + sumstr #拼接当前字符串
        else:
            sumstr = one_str + sumstr #正常拼接字符串
    return sumstr #返回拼接的字符串

# 从 Interbot 那边抄的
mod_list={
    0: 'NONE',
    1: 'NF',
    2: 'EZ',
    3: 'NV',
    4: 'HD',
    5: 'HR',
    6: 'SD',
    7: 'DT',
    8: 'Relax',
    9: 'HT',
    10: 'NC',
    11: 'FL',
    12: 'AT',
    13: 'SO',
    14: 'AP',
    15: 'PF',
    16: 'PF',

}

def getMod(num):
    '''NC出现的话删除DT，PF出现的话删除SD'''
    mods = []
    num = int(num)
    i=1
    while num:
        if num&0x1:
            mods.append(mod_list.get(i))
        num=num>>1
        i+=1
    if not mods:
        return ['NONE']
    if 'NC' in mods:
        mods.remove('DT')
    if 'PF' in mods:
        mods.remove('SD')

    return mods

class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="osu", invoke_without_command=True)
    async def Osuhelpcommand(self, ctx):
        embed=discord.Embed (description = jdata['helptext'])
        embed.set_author(name="osu! command help", url='https://github.com/Kotoki1337/Discord-Toki-bot',icon_url='https://i.ppy.sh/ded4eea5bfcb4c72d3b2f5859c23d3c358aa6b84/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f4272616e645f6964656e746974795f67756964656c696e65732f696d672f75736167652d73696e676c652d636f6c6f75722e706e67')
        await ctx.channel.send(embed=embed)

    @Osuhelpcommand.command(name="chinese", invoke_without_command=True)
    async def OsuhelpCNcommand(self, ctx):
        embed=discord.Embed (description = jdata['helptextCN'])
        embed.set_author(name="osu! 指令功能查询", url='https://github.com/Kotoki1337/Discord-Toki-bot',icon_url='https://i.ppy.sh/ded4eea5bfcb4c72d3b2f5859c23d3c358aa6b84/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f4272616e645f6964656e746974795f67756964656c696e65732f696d672f75736167652d73696e676c652d636f6c6f75722e706e67')
        await ctx.channel.send(embed=embed)

    # bancho v2
    @commands.group(name="bancho", invoke_without_command=True)
    async def Banchocommand(self, ctx):
        embed=discord.Embed (description = jdata['helptext'])
        embed.set_author(name="osu! command help", url='https://github.com/Kotoki1337/Discord-Toki-bot',icon_url='https://i.ppy.sh/ded4eea5bfcb4c72d3b2f5859c23d3c358aa6b84/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f4272616e645f6964656e746974795f67756964656c696e65732f696d672f75736167652d73696e676c652d636f6c6f75722e706e67')
        await ctx.channel.send(embed=embed)

    @Banchocommand.command(name="user")
    async def user_subcommand(self, ctx, msg, *msg2):
        try:
            (m,) = msg2
        except ValueError:
            m = '0'

        apikey = jdata['osu_apikey']
        url = f'https://osu.ppy.sh/api/get_user?k={apikey}&u={msg}&m={m}'

        r = requests.get(url)
        data = r.json()

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

        username = data[0]['username']
        uid = data[0]['user_id']
        pp = data[0]['pp_raw']
        pp_rank = parse_int(data[0]['pp_rank'])
        pp_country_rank = parse_int(data[0]['pp_country_rank'])
        country = data[0]['country']
        accuracy = float(data[0]['accuracy'])
        pc = parse_int(data[0]['playcount'])
        rank_score = parse_int(data[0]['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} stats",
            url=f'https://osu.ppy.sh/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.ppy.sh/{uid}')
        embed.set_author(name="osu!bancho Profile", url=f'https://osu.ppy.sh/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    @Banchocommand.command(name="pr")
    async def recent_subcommand(self, ctx, msg, *msg2):
        try:
            (m,) = msg2
        except ValueError:
            m = '0'

        apikey = jdata['osu_apikey']
        url = f'https://osu.ppy.sh/api/get_user_recent?k={apikey}&u={msg}&m={m}'

        r = requests.get(url)
        data = r.json()

        if m == 0:
            mode = 'std'
        elif m == 1:
            mode = 'taiko'
        elif m == 2:
            mode = 'ctb'
        elif m == 3:
            mode = 'mania'
        else:
            mode = 'std'

        combo = data[0]['maxcombo']
        n300 = data[0]['count300']
        n100 = data[0]['count100']
        n50 = data[0]['count50']
        miss = data[0]['countmiss']
        bid = data[0]['beatmap_id']
        rank = data[0]['rank']
        score = parse_int(data[0]['score'])
        accuracy = '自己算'

        bm = requests.get(f'https://osu.ppy.sh/api/get_beatmaps?k={apikey}&b={bid}')
        bmdata = bm.json()
        song_name = bmdata[0]['title']
        artist = bmdata[0]['artist']
        set_bid = bmdata[0]['beatmapset_id']
        max_combo = bmdata[0]['max_combo']
        diff = bmdata[0]['version']
        star = float(bmdata[0]['difficultyrating'])

        userr = requests.get(f'https://osu.ppy.sh/api/get_user?k={apikey}&u={msg}')
        userdata = userr.json()
        uid = userdata[0]['user_id']
        username = userdata[0]['username']

        mod = getMod(data[0]['enabled_mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {accuracy}\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{artist} - {song_name}[{diff}][{round(star,2)}★]', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.ppy.sh/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: 自己算\n**If**:\n我也不知道多少ACC FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu!bancho with {mode}')
        await ctx.channel.send(embed=embed)

    # 国服 v1
    @commands.group(name="ppy.sb", invoke_without_command=True)
    async def Osusbcommand(self, ctx):
        embed=discord.Embed(description = jdata['helptext'])
        embed.set_author(name="osu! command help", url='https://github.com/Kotoki1337/Discord-Toki-bot',icon_url='https://i.ppy.sh/ded4eea5bfcb4c72d3b2f5859c23d3c358aa6b84/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f4272616e645f6964656e746974795f67756964656c696e65732f696d672f75736167652d73696e676c652d636f6c6f75722e706e67')
        await ctx.channel.send(embed=embed)

    # get user
    @Osusbcommand.command(name="user")
    async def usersb_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/full?id={msg1}'
        else:
            url = f'https://osu.ppy.sb/api/v1/users/full?name={msg1}'
        r = requests.get(url)
        data = r.json()

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
        pp = parse_int(data[f'{mode}']['pp'])
        pp_rank = parse_int(data[f'{mode}']['global_leaderboard_rank'])
        pp_country_rank = parse_int(data[f'{mode}']['country_leaderboard_rank'])
        accuracy = data[f'{mode}']['accuracy']
        pc = parse_int(data[f'{mode}']['playcount'])
        rank_score = parse_int(data[f'{mode}']['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} stats",
            url=f'https://osu.ppy.sb/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.ppy.sb/{uid}')
        embed.set_author(name="osu!ppy.sb Profile", url=f'https://osu.ppy.sb/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    # get rx user
    @Osusbcommand.command(name="rx")
    async def userrxsb_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/rxfull?id={msg1}'
        else:
            url = f'https://osu.ppy.sb/api/v1/users/rxfull?name={msg1}'
        r = requests.get(url)
        data = r.json()

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
        pp = parse_int(data[f'{mode}']['pp'])
        pp_rank = parse_int(data[f'{mode}']['global_leaderboard_rank'])
        pp_country_rank = parse_int(data[f'{mode}']['country_leaderboard_rank'])
        accuracy = data[f'{mode}']['accuracy']
        pc = parse_int(data[f'{mode}']['playcount'])
        rank_score = parse_int(data[f'{mode}']['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} Relax stats",
            url=f'https://osu.ppy.sb/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.ppy.sb/{uid}')
        embed.set_author(name="osu!ppy.sb Profile", url=f'https://osu.ppy.sb/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    # pr
    @Osusbcommand.command(name="pr")
    async def prsb_subcommand(self, ctx, msg1):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/scores/recent?id={msg1}'
            userurl = f'https://osu.ppy.sb/api/v1/users?id={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']
        else:
            url = f'https://osu.ppy.sb/api/v1/users/scores/recent?name={msg1}'
            userurl = f'https://osu.ppy.sb/api/v1/users?name={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']

        r = requests.get(url)
        data = r.json()

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
        score = parse_int(data['scores'][0]['score'])
        accuracy = data['scores'][0]['accuracy']

        mod = getMod(data['scores'][0]['mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {round(accuracy,2)}%\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.ppy.sb/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: {round(current_pp,2)}pp\n**If**:\n{round(accuracy,2)}% FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu.ppy.sb with {mode}')
        await ctx.channel.send(embed=embed)

    # prrx
    @Osusbcommand.command(name="prrx")
    async def prrxsb_subcommand(self, ctx, msg1):
        if msg1.isdigit():
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?id={msg1}'
            userurl = f'https://osu.ppy.sb/api/v1/users?id={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']
        else:
            url = f'https://osu.ppy.sb/api/v1/users/scores/rxrecent?name={msg1}'
            userurl = f'https://osu.ppy.sb/api/v1/users?name={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']

        r = requests.get(url)
        data = r.json()

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
        score = parse_int(data['scores'][0]['score'])
        accuracy = data['scores'][0]['accuracy']

        mod = getMod(data['scores'][0]['mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {round(accuracy,2)}%\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.ppy.sb/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: {round(current_pp,2)}pp\n**If**:\n{round(accuracy,2)}% FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu.ppy.sb with {mode} Relax')
        await ctx.channel.send(embed=embed)

    # Kawata v1
    @commands.group(name="kawata", invoke_without_command=True)
    async def Kawatacommand(self, ctx):
        embed=discord.Embed(description = jdata['helptext'])
        embed.set_author(name="osu! command help", url='https://github.com/Kotoki1337/Discord-Toki-bot',icon_url='https://i.ppy.sh/ded4eea5bfcb4c72d3b2f5859c23d3c358aa6b84/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f4272616e645f6964656e746974795f67756964656c696e65732f696d672f75736167652d73696e676c652d636f6c6f75722e706e67')
        await ctx.channel.send(embed=embed)

    @Kawatacommand.command(name="user")
    async def userkawata_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://kawata.pw/api/v1/users/full?id={msg1}'
        else:
            url = f'https://kawata.pw/api/v1/users/full?name={msg1}'
        r = requests.get(url)
        data = r.json()

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
        pp = parse_int(data[f'{mode}']['pp'])
        pp_rank = parse_int(data[f'{mode}']['global_leaderboard_rank'])
        pp_country_rank = parse_int(data[f'{mode}']['country_leaderboard_rank'])
        accuracy = data[f'{mode}']['accuracy']
        pc = parse_int(data[f'{mode}']['playcount'])
        rank_score = parse_int(data[f'{mode}']['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} **cheating** stats",
            url=f'https://kawata.pw/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.kawata.pw/{uid}')
        embed.set_author(name="osu!kawata Profile", url=f'https://kawata.pw/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    # pr
    @Kawatacommand.command(name="pr")
    async def prkawata_subcommand(self, ctx, *, msg1):
        if msg1.isdigit():
            url = f'https://kawata.pw/api/v1/users/scores/recent?id={msg1}'
            userurl = f'https://kawata.pw/api/v1/users?id={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']
        else:
            url = f'https://kawata.pw/api/v1/users/scores/recent?name={msg1}'
            userurl = f'https://kawata.pw/api/v1/users?name={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']

        r = requests.get(url)
        data = r.json()

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
        score = parse_int(data['scores'][0]['score'])
        accuracy = data['scores'][0]['accuracy']

        mod = getMod(data['scores'][0]['mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {round(accuracy,2)}%\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.kawata.pw/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.kawata.pw/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: {round(current_pp,2)}pp\n**If**:\n{round(accuracy,2)}% FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu!kawata with {mode}')
        await ctx.channel.send(embed=embed)

    # Ripple v1
    @commands.group(name="ripple", invoke_without_command=True)
    async def Ripplecommand(self, ctx):
        embed=discord.Embed(description = jdata['helptext'])
        embed.set_author(name="osu! command help", url='https://github.com/Kotoki1337/Discord-Toki-bot',icon_url='https://i.ppy.sh/ded4eea5bfcb4c72d3b2f5859c23d3c358aa6b84/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f4272616e645f6964656e746974795f67756964656c696e65732f696d672f75736167652d73696e676c652d636f6c6f75722e706e67')
        await ctx.channel.send(embed=embed)

    @Ripplecommand.command(name="user")
    async def userripple_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://ripple.moe/api/v1/users/full?id={msg1}'
        else:
            url = f'https://ripple.moe/api/v1/users/full?name={msg1}'
        r = requests.get(url)
        data = r.json()

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
        pp = parse_int(data[f'{mode}']['pp'])
        pp_rank = parse_int(data[f'{mode}']['global_leaderboard_rank'])
        pp_country_rank = parse_int(data[f'{mode}']['country_leaderboard_rank'])
        accuracy = data[f'{mode}']['accuracy']
        pc = parse_int(data[f'{mode}']['playcount'])
        rank_score = parse_int(data[f'{mode}']['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} stats",
            url=f'https://ripple.moe/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.ripple.moe/{uid}')
        embed.set_author(name="osu!ripple Profile", url=f'https://ripple.moe/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    @Ripplecommand.command(name="rx")
    async def userrxripple_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://ripple.moe/api/v1/users/full?id={msg1}&relax=1'
        else:
            url = f'https://ripple.moe/api/v1/users/full?name={msg1}&relax=1'
        r = requests.get(url)
        data = r.json()

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
        pp = parse_int(data[f'{mode}']['pp'])
        pp_rank = parse_int(data[f'{mode}']['global_leaderboard_rank'])
        pp_country_rank = parse_int(data[f'{mode}']['country_leaderboard_rank'])
        accuracy = data[f'{mode}']['accuracy']
        pc = parse_int(data[f'{mode}']['playcount'])
        rank_score = parse_int(data[f'{mode}']['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} Relax stats",
            url=f'https://ripple.moe/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.ripple.moe/{uid}')
        embed.set_author(name="osu!ripple Profile", url=f'https://ripple.moe/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    # pr
    @Ripplecommand.command(name="pr")
    async def prripple_subcommand(self, ctx, *, msg1):
        if msg1.isdigit():
            url = f'https://ripple.moe/api/v1/users/scores/recent?id={msg1}'
            userurl = f'https://ripple.moe/api/v1/users?id={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']
        else:
            url = f'https://ripple.moe/api/v1/users/scores/recent?name={msg1}'
            userurl = f'https://ripple.moe/api/v1/users?name={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']

        r = requests.get(url)
        data = r.json()

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
        score = parse_int(data['scores'][0]['score'])
        accuracy = data['scores'][0]['accuracy']

        mod = getMod(data['scores'][0]['mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {round(accuracy,2)}%\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.osu.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.ripple.moe/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: {round(current_pp,2)}pp\n**If**:\n{round(accuracy,2)}% FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu!ripple with {mode}')
        await ctx.channel.send(embed=embed)

    @Ripplecommand.command(name="prrx")
    async def prrxripple_subcommand(self, ctx, *, msg1):
        if msg1.isdigit():
            url = f'https://ripple.moe/api/v1/users/scores/recent?id={msg1}&relax=1'
            userurl = f'https://ripple.moe/api/v1/users?id={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']
        else:
            url = f'https://ripple.moe/api/v1/users/scores/recent?name={msg1}&relax=1'
            userurl = f'https://ripple.moe/api/v1/users?name={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']

        r = requests.get(url)
        data = r.json()

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
        score = parse_int(data['scores'][0]['score'])
        accuracy = data['scores'][0]['accuracy']

        mod = getMod(data['scores'][0]['mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {round(accuracy,2)}%\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.ripple.moe/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: {round(current_pp,2)}pp\n**If**:\n{round(accuracy,2)}% FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu!ripple with {mode} Relax')
        await ctx.channel.send(embed=embed)

    # Akatsuki v1
    @commands.group(name="akatsuki", invoke_without_command=True)
    async def Akatsukicommand(self, ctx):
        embed=discord.Embed(description = jdata['helptext'])
        embed.set_author(name="osu! command help", url='https://github.com/Kotoki1337/Discord-Toki-bot',icon_url='https://i.ppy.sh/ded4eea5bfcb4c72d3b2f5859c23d3c358aa6b84/68747470733a2f2f6f73752e7070792e73682f68656c702f77696b692f4272616e645f6964656e746974795f67756964656c696e65732f696d672f75736167652d73696e676c652d636f6c6f75722e706e67')
        await ctx.channel.send(embed=embed)

    @Akatsukicommand.command(name="user")
    async def useraka_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://akatsuki.pw/api/v1/users/full?id={msg1}'
        else:
            url = f'https://akatsuki.pw/api/v1/users/full?name={msg1}'
        r = requests.get(url)
        data = r.json()

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
        pp = parse_int(data[f'{mode}']['pp'])
        pp_rank = parse_int(data[f'{mode}']['global_leaderboard_rank'])
        pp_country_rank = parse_int(data[f'{mode}']['country_leaderboard_rank'])
        accuracy = data[f'{mode}']['accuracy']
        pc = parse_int(data[f'{mode}']['playcount'])
        rank_score = parse_int(data[f'{mode}']['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} stats",
            url=f'https://akatsuki.pw/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.akatsuki.pw/{uid}')
        embed.set_author(name="osu!akatsuki.pw Profile", url=f'https://akatsuki.pw/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    @Akatsukicommand.command(name="rx")
    async def userrxaka_subcommand(self, ctx, msg1, *msg2):
        if msg1.isdigit():
            url = f'https://akatsuki.pw/api/v1/users/rxfull?id={msg1}'
        else:
            url = f'https://akatsuki.pw/api/v1/users/rxfull?name={msg1}'
        r = requests.get(url)
        data = r.json()

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
        pp = parse_int(data[f'{mode}']['pp'])
        pp_rank = parse_int(data[f'{mode}']['global_leaderboard_rank'])
        pp_country_rank = parse_int(data[f'{mode}']['country_leaderboard_rank'])
        accuracy = data[f'{mode}']['accuracy']
        pc = parse_int(data[f'{mode}']['playcount'])
        rank_score = parse_int(data[f'{mode}']['ranked_score'])

        embed=discord.Embed (
            title=f"{username}'s {mode} Relax stats",
            url=f'https://akatsuki.pw/users/{uid}',
            description=f"**Rank**: #{pp_rank}({country}#{pp_country_rank})\n**Performance**: {pp}\n**Accuracy**: {round(accuracy,2)}%\n**Play Count**: {pc}\n**Ranked score**: {rank_score}"
        )
        embed.set_thumbnail(url=f'https://a.akatsuki.pw/{uid}')
        embed.set_author(name="osu!akatsuki Profile", url=f'https://akatsuki.pw/users/{uid}',icon_url=f'https://osu.ppy.sh/images/flags/{country}.png')
        await ctx.channel.send(embed=embed)

    # pr
    @Akatsukicommand.command(name="pr")
    async def praka_subcommand(self, ctx, *, msg1):
        if msg1.isdigit():
            url = f'https://akatsuki.pw/api/v1/users/scores/recent?id={msg1}'
            userurl = f'https://akatsuki.pw/api/v1/users?id={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']
        else:
            url = f'https://akatsuki.pw/api/v1/users/scores/recent?name={msg1}'
            userurl = f'https://akatsuki.pw/api/v1/users?name={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']

        r = requests.get(url)
        data = r.json()

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
        score = parse_int(data['scores'][0]['score'])
        accuracy = data['scores'][0]['accuracy']

        mod = getMod(data['scores'][0]['mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {round(accuracy,2)}%\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.osu.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.akatsuki.pw/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: {round(current_pp,2)}pp\n**If**:\n{round(accuracy,2)}% FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu!akatsuki with {mode}')
        await ctx.channel.send(embed=embed)

    @Akatsukicommand.command(name="prrx")
    async def prrxaka_subcommand(self, ctx, *, msg1):
        if msg1.isdigit():
            url = f'https://akatsuki.pw/api/v1/users/scores/rxrecent?id={msg1}&relax=1'
            userurl = f'https://akatsuki.pw/api/v1/users?id={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']
        else:
            url = f'https://akatsuki.pw/api/v1/users/scores/rxrecent?name={msg1}&relax=1'
            userurl = f'https://akatsuki.pw/api/v1/users?name={msg1}'
            ru = requests.get(userurl)
            userdata = ru.json()
            username = userdata['username']
            uid = userdata['id']

        r = requests.get(url)
        data = r.json()

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
        score = parse_int(data['scores'][0]['score'])
        accuracy = data['scores'][0]['accuracy']

        mod = getMod(data['scores'][0]['mods'])
        mod = ", ".join(str(i) for i in mod)

        embed=discord.Embed(
                        description=f'**User**: {username} (Uid: {uid})\n**Combo**: {combo}/{max_combo}\n{n300}x **300** | {n100}x **100** | {n50}x **50** | {miss} **miss**\n**Accuracy**: {round(accuracy,2)}%\n**Rank**: {rank}\n**Mods**: {mod}\n**Scores**: {score}')
        embed.set_thumbnail(url=f'https://b.ppy.sh/thumb/{set_bid}l.jpg')
        embed.set_author(name=f'{song_name}', url=f'https://osu.ppy.sh/b/{bid}',icon_url=f'https://a.akatsuki.pw/{uid}')
        embed.add_field(name='Performance', value=f'**Current PP**: {round(current_pp,2)}pp\n**If**:\n{round(accuracy,2)}% FC = Unknownpp\n100% SS = Unknownpp', inline=False)
        embed.set_footer(text=f'Played on osu!akatsuki with {mode} Relax')
        await ctx.channel.send(embed=embed)
def setup(bot):
    bot.add_cog(Osu(bot))