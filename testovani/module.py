import discord
import tempfile
import json
from discord.ext import commands

from core import acl, text, logging

class Testovani(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rawGr(self, ctx):
        await ctx.send(ctx.guild.by_category())

    @commands.command()
    async def descr(self, ctx):
        ans = []
        categories = ctx.guild.by_category()
        for category in categories:
            channels = category[1]
            for channel in channels:
                ans.append(channel.topic)
        await ctx.send(ans)
    @commands.command()
    async def groups(self, ctx):



        if len(ctx.message.attachments) != 1:
            await ctx.send("Only 1 file allowed as an attachment.")
            return
        if not ctx.message.attachments[0].filename.lower.endswith("json"):
            await ctx.send("Only .json files allowed as an attachment.")
            return
        # download the file
        # similiar code that was used for a reference: main/modules/base/acl/module.py/line 276
        data_file = tempfile.TemporaryFile()
        await ctx.message.attachments[0].save(data_file)
        data_file.seek(0)
        try:
            json_data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            await ctx.send("This file seems corrupted.")
            return
        # loading data from .json file
        institutes = []
        for subject in json_data:
            if subject['institute'] not in institutes:
                institutes.append(subject)

        categories = ctx.guild.by_category()
        categoriesToCompare = []
        categoryNames = []
        channelNames = []
        for category in categories:
            categoryName = str(category[0]).lower()
            if categoryName not in categoryNames:
                if categoryName in institutes:
                    categoriesToCompare.append(category)


        for institute in institutes:
            category = None
            for category in categories:
                if str(category[0]).lower() == institute.name.lower():
                    break
            #for subject

            #for subject in institute:
            #    if subject not in



            channels = category[1]
            for channel in channels:
                channelNames.append(str(channel).lower())


        for institute in institutes:
            names = []
            abbrs = []
            for subject in institute:
                if subject['name'] not in names:
                    names.append(subject['name'].lower())
                if subject['abbreviation'] not in abbrs:
                    abbrs.append(subject['abbreviation'].lower())
        # loading data from guild
        await ctx.send(str(categoryNames)+str(channelNames))

def setup(bot) -> None:
    bot.add_cog(Testovani(bot))