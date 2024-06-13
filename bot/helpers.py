
import discord
import json

from utils import io

async def is_authorized(ctx: discord.ApplicationContext): 
    config = io.load_json("data/config.json")

    if not ctx.author.id in config['owners']:
        return await ctx.respond(embed=discord.Embed(description="# You are not authorized to use this command."))

    return True