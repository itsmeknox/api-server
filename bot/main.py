from discord.ext import commands
from utils import io

from .helpers import (
    is_authorized
)

from modules.constants import config



import discord
import threading

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.slash_command(name="change-properties")
async def change_properties(ctx: discord.ApplicationContext, super_x_properties: str, useragent: str):
    if not await is_authorized(ctx):
        return

    await ctx.defer()

    properties = io.load_json('data/properties.json')
    if super_x_properties:
        properties['x_super'] = super_x_properties
    if useragent:
        properties['useragent'] = useragent

    io.save_json("data/properties.json", properties)
    
    await ctx.respond(embed=discord.Embed(description=f"# Successfully Updated Propertes\n> **Useragent:** {useragent}\n\n> **Super X Properties:** {super_x_properties}"))



def run_bot():
    threading.Thread(target=bot.run, kwargs={"token": config['bot_token']}).start()
    return True
