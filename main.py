#===============================================================================
# Discord Games Bot v1.1
# - Last Updated: 25 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 25 Apr 2021 - Added config file for the prefix and key. Added discord intents
# 23 Apr 2021 - Error output for non-command messages disabled by TN. -YJ
# 18 Apr 2021 - Started and finished file. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Get the bot key from an env instead of relying on command line input. -YJ
# - Make it possible for a server to change their command_prefix. -YJ
#===============================================================================
# Description
# ..............................................................................
# main.py initializes the Discord bot.
# It logs into Discord as the bot account, and loads all game cogs.
# Run this file with `py -3 main.py ["KEY"]` in the command line on Windows.
#===============================================================================

#Import Modules
import discord
from discord.ext import commands
import sys
import os
import json
with open("./config.json") as config_file:
    config = json.load(config_file)

#Define bot client and command prefix
client = commands.Bot(command_prefix=config["prefix"], intents=discord.Intents.all())
#TODO: Make it possible for a server to change their command_prefix

#Report successful login
@client.event
async def on_ready():
    print("Games Bot online.")

#Skips the error output of non-command messages starting with the prefix
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MemberNotFound):
        return
    raise error

#(Re)load Cogs
    #Unloading specific cogs
@client.command(aliases=[])
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    print(f"Unloaded {extension} cog.")

    #Loading specific cogs
@client.command(aliases=[])
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    print(f"Loaded {extension} cog.")

    #Reloading specific cogs
@client.command(aliases=[])
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    print(f"Reloaded {extension} cog.")

    #Reloading all cogs
@client.command(aliases=["reloadall"])
async def reload_all(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            client.load_extension(f"cogs.{filename[:-3]}")
    print(f'Reloaded all cogs.')

#Loading cogs at startup
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

#Login
client.run(config["token"])
