#===============================================================================
# Hangman v0.1
# - Last Updated: 18 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 18 Apr 2021 - Started and finished file.
#===============================================================================
# Notes
# ..............................................................................
# - Code this. -YJ
#===============================================================================
# Description
# ..............................................................................
# hangman.py plays a game where player(s) take turns guessing letters in an
# attempt to deduce a word. One user has to privately choose the word.
# The bot can take this role by choosing a word from a dictionary.
#===============================================================================

#Import Modules
import discord
from discord.ext import commands

#Cog Setup
class Hangman(commands.Cog):
    #Define variables.
    def __init__(self, client):
        self.client = client

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Hangman cog loaded.")

    #Play hangman
    @commands.command(aliases=["hm"])
    async def hangman(self, ctx):
        """
        Code goes here
        """

#Client Setup
def setup(client):
    client.add_cog(Hangman(client))
