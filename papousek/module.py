import discord
from discord.ext import commands

from core import acl, text, logging

class Papousek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot) -> None:
    bot.add_cog(Papousek(bot))

@commands.command()
async def papousek(ctx, message):
    await ctx.send(message)