#===============================================================================
# Main Menu v1.1
# - Last Updated: 30 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 04 Jun 2021 - Forgot to actually start the inactivity timer, fixed; Message
#               now gives feedback to when the timer timed out. -YJ
# 02 Jun 2021 - Added inactivity timer to sessions. -YJ
# 30 May 2021 - File started and finished. -YJ
#===============================================================================
# Notes
# ..............................................................................
#
#===============================================================================
# Description
# ..............................................................................
# The main menu displays a list of games available through the bot and lets
# users start a new game through text command or reaction.
#===============================================================================

#Import Modules
import discord
from discord.ext import commands, tasks

class MainMenuSession:
    def __init__(self, ctx, parent, message_menu):
        self.__ctx = ctx
        self.__parent = parent
        self.__message_menu = message_menu
        self.inactivity_timer.start()

    @property
    def ctx(self):
        return self.__ctx

    @property
    def message_menu(self):
        return self.__message_menu

    #Inactivity timer.
    @tasks.loop(minutes=10.0, count=2)
    async def inactivity_timer(self):
        if self.inactivity_timer.current_loop != 0:
            await self.__parent.timeout_session(self)

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

    #Remove session on inactivity timeout. Override if needed.
    async def timeout_session(self, session):
        msg = session.message_menu.content + "\n"
        msg += "Reactions have timed out. Use the text command or call for a new main menu message."
        await session.message_menu.edit(content=msg)
        await session.message_menu.clear_reactions()
        self.menu_sessions.remove(session)

    #Primary Functions
    #With no arguments specified, send game instructions.
    @commands.group(name="mainmenu", aliases=["main_menu", "main", "menu", "games", "game", "list", "games_list", "game_list", "gameslist", "gamelist"], case_insensitive=True, invoke_without_command=True)
    async def mainmenu(self, ctx):
        msg = "**Main Menu**\n"
        msg += "1️⃣ - `!bj` - Blackjack\n"
        msg += "2️⃣ - `!ch` - Checkers\n"
        msg += "3️⃣ - `!c4` - Connect Four\n"
        msg += "4️⃣ - `!hm` - Hangman\n"
        msg += "5️⃣ - `!ttt` - Tic-tac-toe"
        message_menu = await ctx.channel.send(msg)
        self.menu_sessions.append(MainMenuSession(ctx, self, message_menu))
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
