from copy import copy

import discord
import tempfile
import json
from discord.ext import commands
from discord import ChannelType

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
                if channel.type == ChannelType.text:
                    ans.append(channel.topic)
                else:
                    continue
        await ctx.send(ans)

    @commands.command()
    async def groups(self, ctx):
        """Check subjects' text channels with a json file."""
        if len(ctx.message.attachments) != 1:
            await ctx.send("Only 1 file allowed as an attachment.")
            return
        if not ctx.message.attachments[0].filename.lower().endswith("json"):
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
            if subject['institute'].lower() not in institutes:
                institutes.append(subject['institute'].lower())
        categories = ctx.guild.by_category()

        # loading institutes
        for institute in institutes:
            correctChannels = 0
            await ctx.send("Institute: **%s**" % institute)
            instituteSubjects = []
            for subject in json_data:
                if subject['institute'].lower() == institute:
                    instituteSubjects.append(subject)
            # looking for institutes' channel categories
            category = None
            categoryFound = False
            for category in categories:
                if str(category[0]).lower() == institute: # category[0] is it's header, [1] are channels
                    categoryFound = True
                    break
            if not categoryFound:
                await ctx.send("Category %s not found on this server." % institute)
                continue
            # fetching channel names and descriptions
            channels = category[1]
            chNames = []
            chDescrs = []
            for channel in channels:
                chNames.append(str(channel.name).lower())
                chDescrs.append(str(channel.topic).lower())
            chNamesCp = copy(chNames) # this will hold redundant channels
            # comparing subject abbreviations and names to the .json file
            subjectIndex = 0
            for subject in instituteSubjects:
                sAbbr = subject['abbreviation'].lower()
                correctAbbr = False
                # searching for a correct channel by name
                for chName in chNames:
                    if chName == sAbbr:
                        correctAbbr = True
                        chNamesCp.remove(sAbbr)
                        chNames.index(str(sAbbr))
                        print(subjectIndex)
                        #await ctx.send("Channel %s found." % sAbbr)
                        break
                if not correctAbbr:
                    await ctx.send("Channel %s not found." % sAbbr)
                    continue
                sName = subject['name'].lower()
                #checking if the subject's name matches it's abrreviation
                if chDescrs[subjectIndex] == sName:
                    #await ctx.send("Channel description %s found." % sName)
                    correctChannels += 1
                else:
                    await ctx.send("Channel %s has a faulty description" % sAbbr)
            await ctx.send("Correct channels for institute **%s**: %d" % (institute, correctChannels))
            if len(chNamesCp) != 0:
                rooms = ""
                for redundantRoom in chNamesCp:
                    rooms += (redundantRoom+"\n")
                await ctx.send("Redundant channels for %s:\n%s" % (institute, rooms))
        await ctx.send("Done!")

def setup(bot) -> None:
    bot.add_cog(Testovani(bot))