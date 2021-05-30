#===============================================================================
# Main Menu v1.0
# - Last Updated: 30 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 30 May 2021 - File started and finished. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Menu messages pile up and never time out, which is a pretty huge deal.
#   Implement a time-out, preferably along with room ID time-outs. -YJ
#===============================================================================
# Description
# ..............................................................................
# The main menu displays a list of games available through the bot and lets
# users start a new game through text command or reaction.
#===============================================================================

#Import Modules
import discord
from discord.ext import commands

class MainMenuSession:
    def __init__(self, ctx, message_menu):
        self.__ctx = ctx
        self.__message_menu = message_menu

    @property
    def ctx(self):
        return self.__ctx

    @property
    def message_menu(self):
        return self.__message_menu

#Cog Class
class MainMenuCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.menu_sessions = []

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Main Menu cog loaded.")

    #Secondary Functions
    #Game instructions
    def instructions(self):
        msg = "**Main Menu Help**\n"
        msg += "The main menu shows all games available for play. Select one with the specified command or reaction!"
        return msg

    #Primary Functions
    #With no arguments specified, send game instructions.
    @commands.group(name="mainmenu", aliases=["main_menu", "main", "menu", "games", "game", "list", "games_list", "game_list", "gameslist", "gamelist"], invoke_without_command=True)
    async def mainmenu(self, ctx):
        msg = "**Main Menu**\n"
        msg += "1️⃣ - `!bj` - Blackjack\n"
        msg += "2️⃣ - `!ch` - Checkers\n"
        msg += "3️⃣ - `!c4` - Connect Four\n"
        msg += "4️⃣ - `!hm` - Hangman\n"
        msg += "5️⃣ - `!ttt` - Tic-tac-toe"
        message_menu = await ctx.channel.send(msg)
        self.menu_sessions.append(MainMenuSession(ctx, message_menu))
        await message_menu.add_reaction("1️⃣")
        await message_menu.add_reaction("2️⃣")
        await message_menu.add_reaction("3️⃣")
        await message_menu.add_reaction("4️⃣")
        await message_menu.add_reaction("5️⃣")

    #Help command to receive instructions.
    @mainmenu.command(aliases=["?", "info", "information", "instructions"])
    async def help(self, ctx):
        await ctx.channel.send(self.instructions())

    #Reaction handling
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #Prevent bot's own reactions triggering this
        if user == self.client.user:
            return
        for session in self.menu_sessions:
            #Starting game by reacting with appropriate emoji
            if reaction.message.id == session.message_menu.id:
                ctx = await self.client.get_context(reaction.message)
                ctx.author = user
                command = None
                if reaction.emoji == "1️⃣":
                    command = self.client.get_command("blackjack new")
                elif reaction.emoji == "2️⃣":
                    command = self.client.get_command("checkers new")
                elif reaction.emoji == "3️⃣":
                    command = self.client.get_command("connectfour new")
                elif reaction.emoji == "4️⃣":
                    command = self.client.get_command("hangman new")
                elif reaction.emoji == "5️⃣":
                    command = self.client.get_command("tictactoe new")
                if command != None:
                    await ctx.invoke(command)
                return

#Client Setup
def setup(client):
    client.add_cog(MainMenuCog(client))
