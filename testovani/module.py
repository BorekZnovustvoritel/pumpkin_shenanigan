import discord
from discord.ext import commands

from core import acl, text, logging

class Testovani(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def groups(self, ctx):
        categories = ctx.guild.by_category()
        categoryNames = []
        names = []
        for category in categories:
            header = category[0]
            if header['name'] not in categoryNames:
                categoryNames.append(header['name'])
            rooms = category[1]
            for room in rooms:
                if room[1] not in names:
                    names.append(room[1])
        await ctx.send(str(categoryNames)+str(names))

    #@commands.command()
    #async def channels(self, ctx):
    #    await ctx.send(ctx.guild.fetch_channels())

def setup(bot) -> None:
    bot.add_cog(Testovani(bot))