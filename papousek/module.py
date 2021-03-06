import discord
import time
from discord.ext import commands

from core import acl, text, logging

class Papousek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def papousek(self, ctx, *, message = None):
        """Zopakuju po tobě, co mi řekneš."""
        if message is None:
            message = "\*Zvuky papouška - jak dělá papoušek? Ó kruci, ó doprčic, já to nevím.\*"
        await ctx.send(message)

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