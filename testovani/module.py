import discord
from discord.ext import commands

from core import acl, text, logging

class Testovani(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def groups(self, ctx):
        await ctx.send(str(ctx.guild))

def setup(bot) -> None:
    bot.add_cog(Testovani(bot))