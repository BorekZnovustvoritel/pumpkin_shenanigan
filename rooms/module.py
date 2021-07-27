import tempfile
import json

import discord

from discord.ext import commands

from core import acl, text, logging

class Rooms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rooms(self, ctx):
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
        for institute in institutes:
            names = []
            abbrs = []
            for subject in institute:
                if subject['name'] not in names:
                    names.append(subject['name'].lower())
                if subject['abbreviation'] not in abbrs:
                    abbrs.append(subject['abbreviation'].lower())
        # loading data from guild
        ctx.message.guild.categories
