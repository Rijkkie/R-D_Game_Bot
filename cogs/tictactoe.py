#===============================================================================
# Tic-tac-toe v1.3
# - Last Updated: 30 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 30 May 2021 - Reaction join now goes through cog's join() instead of Game's
#               join(), which allows for better specialization; Added database
#               support. -YJ
# 24 May 2021 - All classes now extend a base class; max_players is a function
#               again, this time for class flexibility instead of var memory;
#               Fixed a bug that would identify a full board as a tie even if
#               it was not. -YJ
# 16 May 2021 - "msg" string legibility improved, max_players is now a variable,
#               !join no longer case-sensitive, added player list command. -YJ
# 30 Apr 2021 - Added quit feature, react clears; Improved legibility more. -YJ
# 29 Apr 2021 - Added react-to-join feature. -YJ
# 28 Apr 2021 - Saving User instead of User.id now; Added session class;
#               Improved legibility. -YJ
# 22 Apr 2021 - Fixed bug where the gamebot crashes when trying to
#               mention a player. -RK
# 19 Apr 2021 - Hacked together some gameplay code; Finished file. -YJ
# 18 Apr 2021 - Started file; Made room creation code. -YJ
#===============================================================================
# Notes
# ..............................................................................
# 
#===============================================================================
# Description
# ..............................................................................
# tictactoe.py plays a game where two players take turns choosing one tile in a
# 3x3 grid to place their respective tokens. If three tiles in a line hold the
# same player's token, that player wins the game.
#===============================================================================

#Import Modules
import discord
from discord import Message
from discord.ext import commands

from common.session import Session
from common.player import Player
from common.game import Game
from common.emoji import number_to_emoji, emoji_to_number

from database import dbfunctions

import random

#Session Setup
class TictactoeSession(Session):
    #Define variables.
    def __init__(self, game_sessions):
        Session.__init__(self, game_sessions)
        self.__player_turn = 0
        self.__board_state = "123456789"
        self.__message_board = None

    @property
    def player_turn(self):
        return self.__player_turn

    @property
    def board_state(self):
        return self.__board_state

    @property
    def message_board(self):
        return self.__message_board

    @board_state.setter
    def board_state(self, board_state: str):
        self.__board_state = board_state

    @message_board.setter
    def message_board(self, message_board: Message):
        self.__message_board = message_board

    #Set next player turn.
    def next_turn(self):
        self.__player_turn = (self.__player_turn + 1) % len(self.players)

#Cog Setup
class TictactoeCog(Game):
    #Define variables.
    def __init__(self, client):
        Game.__init__(self, client)
        self.instant_start = True
        self.game_name = "Tic-tac-toe"
        self.game_abbrev = "ttt"

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Tictactoe cog loaded.")

    #Secondary Functions
    #Game instructions
    def instructions(self):
        msg = "**Tic-tac-toe Help**\n"
        msg += "A game where two players take turns marking spaces in a three-by-three grid to try and get three of their marks in one line. The game will automatically start when it has two players.\n"
        msg += "`!ttt new`: Start a new room.\n"
        msg += "`!ttt join XXXX`: Join an existing room with its room ID specified in place of XXXX. This also starts the game.\n"
        msg += "`!ttt players XXXX`: Get a list of players in an existing room with its room ID specified in place of XXXX.\n"
        msg += "`!ttt quit XXXX`: Quit a room you're in with its room ID specified in place of XXXX. This also ends the game.\n"
        msg += "`!ttt quit all`: Quit all rooms you're in. This also ends each game."
        return msg

    #Get maximum amount of players of a session.
    def get_max_players(self, session):
        return 2

    #Check board state for a winning position.
    def is_game_won(self, board_state):
        for i in range(3):
            #Check for horizontal wins
            token = board_state[i*3:i*3+1]
            if token == board_state[i*3+1:i*3+2] and token == board_state[i*3+2:i*3+3]:
                return True
            #Check for vertical wins
            token = board_state[i:i+1]
            if token == board_state[i+3:i+4] and token == board_state[i+6:i+7]:
                return True
        #Check for diagonal wins
        token = board_state[4:5]
        if token == board_state[0:1] and token == board_state[8:9] or token == board_state[2:3] and token == board_state[6:7]:
            return True
        return False

    #Check board state for a tie position.
    def is_game_tied(self, board_state):
        for i in range(9):
            if board_state[i] != "x" and board_state[i] != "o":
                return False
        return self.is_game_won(board_state) == False

    #Generate game board message.
    def generate_board_message(self, session):
        msg = f"**Tic-tac-toe Room {session.room_id}**\n"
        msg += f"❌: {session.players[0].user.mention}\n"
        msg += f"⭕: {session.players[1].user.mention}\n"
        for column, tile in enumerate(session.board_state):
            if column % 3 == 0:
                msg += "\n"
            if tile == "x":
                msg += "❌"
                continue
            if tile == "o":
                msg += "⭕"
                continue
            msg += number_to_emoji(column+1)
        if self.is_game_tied(session.board_state) == True:
            msg += "\n\nThe game has ended in a tie!"
            return msg
        msg += f"\n\n{session.players[session.player_turn].user.mention}"
        if self.is_game_won(session.board_state) == True:
            msg += " has won the game!"
            return msg
        msg += "'s turn!"
        return msg

    #Place token in tile, check for winner, edit message and clear reaction.
    async def process_turn(self, session, tile, reaction):
        #Identify token and place it.
        token = "x"
        if session.player_turn == 1:
            token = "o"
        board = session.board_state
        session.board_state = board[:tile-1] + token + board[tile:]
        #If game is won or tied.
        if self.is_game_won(session.board_state) == True or self.is_game_tied(session.board_state) == True:
            #Add result to database
            if self.is_game_won(session.board_state) == True:
                for i, player in enumerate(session.players):
                    if i == session.player_turn:
                        dbfunctions.boardgame_action("TicTacToe", player.user.id, session.message_board.guild.id, 'w')
                    else:
                        dbfunctions.boardgame_action("TicTacToe", player.user.id, session.message_board.guild.id, 'l')
            else:
                for player in enumerate(session.players):
                    dbfunctions.boardgame_action("TicTacToe", player.user.id, session.message_board.guild.id, 'd')
            #End session
            msg = self.generate_board_message(session)
            await reaction.message.edit(content=msg)
            await reaction.message.clear_reactions()
            self.game_sessions.remove(session)
            return
        #If game is unfinished.
        session.next_turn()
        msg = self.generate_board_message(session)
        await reaction.message.edit(content=msg)
        await reaction.message.clear_reaction(reaction.emoji)

    #Generate and send first message.
    async def setup_game(self, session, channel):
        session.shuffle_players()
        msg = self.generate_board_message(session)
        board_message = await channel.send(msg)
        session.message_board = board_message
        for i in range(9):
            reaction = number_to_emoji(i+1)
            await board_message.add_reaction(reaction)
        return

    #Handle additional checks required when a player quits the game.
    async def remove_player(self, session, user):
        session.remove_player(user)
        if session.message_board != None:
            await session.message_board.delete()
        self.game_sessions.remove(session)

    #Primary functions
    #With no arguments specified, send game instructions.
    @commands.group(name="tictactoe", aliases=["ttt", "tic-tac-toe"], invoke_without_command=True)
    async def tictactoe(self, ctx):
        await ctx.channel.send(self.instructions())

    #Help command to receive instructions.
    @tictactoe.command(aliases=["?", "info", "information", "instructions"])
    async def help(self, ctx):
        await ctx.channel.send(self.instructions())

    #See the list of players of a room.
    @tictactoe.command(aliases=["player", "players", "playerlist", "playerslist", "players_list", "list"])
    async def player_list(self, ctx, room_id=None):
        await Game.player_list(self, ctx, room_id)

    #Register a new game room.
    @tictactoe.command(aliases=["start", "begin", "create", "register", "host"])
    async def new(self, ctx):
        session = TictactoeSession(self.game_sessions)
        player = Player(ctx.author)
        await Game.new(self, ctx, session, player)

    #Join an existing game room by message.
    @tictactoe.command(aliases=["enter"])
    async def join(self, ctx, room_id=None):
        player = Player(ctx.author)
        await Game.join(self, ctx, room_id, player)

    #Quit a room.
    @tictactoe.command(aliases=["stop", "exit", "end", "leave"])
    async def quit(self, ctx, room_id=None):
        await Game.quit(self, ctx, room_id)

    #Reaction handling
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #Prevent bot's own reactions triggering this
        if user == self.client.user:
            return
        for session in self.game_sessions:
            #Joining game by reacting with play emoji
            if session.message_join != None and reaction.message.id == session.message_join.id and reaction.emoji == "▶️":
                ctx = await self.client.get_context(reaction.message)
                ctx.author = user
                await self.join(ctx, session.room_id)
                return

            #Taking turn by reacting with number emoji
            if session.message_board != None and reaction.message.id == session.message_board.id:
                if user.id == session.players[session.player_turn].user.id:
                    if reaction.emoji in ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]:
                        #Find which number was reacted with
                        pos = emoji_to_number(reaction.emoji)
                        if str(pos) in session.board_state:
                            await self.process_turn(session, pos, reaction)
                return

#Client Setup
def setup(client):
    client.add_cog(TictactoeCog(client))
