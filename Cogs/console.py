import disnake
import datetime
from disnake.ext import commands


class Console(commands.Cog):
    """ Does the console printing of the bot. """

    def __init__(self, bot):
        """ Set bot attribute. """
        self.bot = bot

    @staticmethod
    def timestamp():
        """ Easy timestamp generation. """
        return datetime.datetime.now().strftime("%x - [%X]")

    @commands.Cog.listener()
    async def on_ready(self):
        print('------')
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print(disnake.__version__)
        print('------')

        print('Servers connected to:')
        # for server in bot.guilds:
        #     print(server)
        print(f"{len(self.bot.guilds)} servers.")
        print('------')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """ Print command calls to the console. """
        print(f'{self.timestamp()}\n    Command: {ctx.command}\n    Sender:  {ctx.author}\n    Guild:   {ctx.guild}\n')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """ Print guild adds to the console. """
        print(f'{self.timestamp()}\n    Bot has been added to guild: {guild}\n')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """ Print guild removes to the console. """
        print(f'{self.timestamp()}\n    Bot has been removed from guild: {guild}\n')

def setup(bot):
    bot.add_cog(Console(bot))
