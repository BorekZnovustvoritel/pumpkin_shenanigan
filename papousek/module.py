import discord
import time
from discord.ext import commands

from core import acl, text, logging

class Papousek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def papousek(self, ctx, *, message):
        """Zopakuju po tobě, co mi řekneš."""
        if message:
            await ctx.send(message)
        else:
            await ctx.send("\*Zvuky papouška - jak dělá papoušek? Ó kruci, ó doprčic, já to nevím.\*")


    @commands.command()
    async def hodiny(self, ctx):
        """Jaký je čas?"""
        now = time.localtime()
        hours = now[3]
        minutes = now[4]
        seconds = now[5]
        await ctx.send("Momentálně je %d h %d min %d s" % (hours, minutes, seconds))

def setup(bot) -> None:
    bot.add_cog(Papousek(bot))