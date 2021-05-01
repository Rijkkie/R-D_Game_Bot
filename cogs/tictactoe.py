#===============================================================================
# Tic-tac-toe v1.1
# - Last Updated: 30 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
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
# - Add an expiry timer on that room ID or something, to prevent users from just
#   starting a bunch of empty rooms and hogging all the IDs. -YJ
#===============================================================================
# Description
# ..............................................................................
# tictactoe.py plays a game where two players take turns choosing one of nine
# tiles to place their respective tokens. If three tiles in a row hold the same
# player's token, that player wins the game.
#===============================================================================

#Import Modules
import discord
from discord import Message, User
from discord.ext import commands
import common
import random

#Session Setup
class TictactoeSession:
    #Define variables.
    def __init__(self, room_id: str):
        self.__room_id = room_id
        self.__players = []
        self.__player_turn = 0
        self.__board_state = "123456789"
        self.__message_board = None
        self.__message_join = None

    @property
    def room_id(self):
        return self.__room_id

    @property
    def players(self):
        return self.__players

    @property
    def player_turn(self):
        return self.__player_turn

    @property
    def board_state(self):
        return self.__board_state

    @property
    def message_board(self):
        return self.__message_board

    @property
    def message_join(self):
        return self.__message_join

    @board_state.setter
    def board_state(self, board_state: str):
        self.__board_state = board_state

    @message_board.setter
    def message_board(self, message_board: Message):
        self.__message_board = message_board

    @message_join.setter
    def message_join(self, message_join: Message):
        self.__message_join = message_join

    #Add players.
    def add_player(self, player: User):
        if player not in self.__players:
            self.__players.append(player)

    #Remove player.
    def remove_player(self, player: User):
        if player in self.__players:
            self.__players.remove(player)

    #Shuffle players.
    def shuffle_players(self):
        random.shuffle(self.__players)

    #Set next player turn.
    def next_turn(self):
        self.__player_turn = (self.__player_turn + 1) % len(self.__players)

#Cog Setup
class TictactoeCog(commands.Cog):
    #Define variables.
    def __init__(self, client):
        self.client = client
        self.game_sessions = []

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Tic-tac-toe cog loaded.")

    #Secondary functions
    #Game instructions
    def instructions(self):
        return "**Tic-tac-toe Help**\nA game where two players take turns marking spaces in a three-by-three grid to try and get three of their marks in one line. The game will automatically start when it has two players.\nStart with `!ttt new`.\nJoin with `!ttt join XXXX` or by reacting to the join message.\nQuit with `!ttt quit XXXX` or `!ttt quit all`."

    #Maximum number of players, as function to save on permanent variable memory
    def max_players(self):
        return 2

    #Check board state for a tie position
    def is_game_tied(self, board_state):
        for i in range(9):
            if board_state[i] != "x" and board_state[i] != "o":
                return False
        return True

    #Check board state for a winning position
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

    #Generate game board message.
    def generate_board_message(self, session):
        msg = f"**Tic-tac-toe Room {session.room_id}**"
        msg += f"\n❌: {session.players[0].mention}"
        msg += f"\n⭕: {session.players[1].mention}\n"
        for column, tile in enumerate(session.board_state):
            if column % 3 == 0:
                msg += "\n"
            if tile == "x":
                msg += "❌"
                continue
            if tile == "o":
                msg += "⭕"
                continue
            msg += common.number_to_emoji(column+1)
        if self.is_game_tied(session.board_state) == True:
            msg += "\n\nThe game has ended in a tie!"
            return msg
        msg += f"\n\n{session.players[session.player_turn].mention}"
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
    async def setup_game(self, channel, session):
        session.shuffle_players()
        msg = self.generate_board_message(session)
        board_message = await channel.send(msg)
        session.message_board = board_message
        for i in range(9):
            reaction = common.number_to_emoji(i+1)
            await board_message.add_reaction(reaction)
        return

    #Attempt to add player to room and give feedback.
    async def join_game(self, channel, game_sessions, room_id, player, max_players):
        return_code = common.join_room(game_sessions, room_id, player, max_players)
        msg = "An unknown error occurred."
        if return_code == 0:
            for session in game_sessions:
                if session.room_id == room_id:
                    await self.setup_game(channel, session)
                    return
        elif return_code == 1:
            msg = f"{player.name} is already in room {room_id}!"
        elif return_code == 2:
            msg = f"Room {room_id} is full."
        elif return_code == 3:
            msg = f"Room {room_id} does not exist."
        await channel.send(content=msg, delete_after=15.0)

    async def quit_game(self, game_sessions, room_id, player):
        return_code = common.quit_room(game_sessions, room_id, player)
        for session in game_sessions:
            if room_id == session.room_id:
                msg = session.message_board.content
                msg += f"\n{player.mention} has forfeited the game."
                await session.message_board.edit(content=msg)
                await session.message_board.clear_reactions()
                self.game_sessions.remove(session)
                return return_code
        return return_code

    #Primary functions
    #With no arguments specified, send game instructions.
    @commands.group(name="tictactoe", aliases=["ttt", "tic-tac-toe"], invoke_without_command=True)
    async def tictactoe(self, ctx):
        await ctx.channel.send(self.instructions())

    #Help command to receive instructions.
    @tictactoe.command(aliases=["?", "info", "information", "instructions"])
    async def help(self, ctx):
        await ctx.channel.send(self.instructions())

    #Register a new game room.
    @tictactoe.command(aliases=["start", "begin", "create", "host"])
    async def new(self, ctx):
        room_id = common.generate_room_id(self.game_sessions)
        #Save new session
        session = TictactoeSession(room_id)
        session.add_player(ctx.author)
        self.game_sessions.append(session)
        #Send session's room ID
        msg = f"New tic-tac-toe room created! Your room ID is: {room_id}.\nOthers can join by typing `!ttt join {room_id}`"
        if ctx.guild != None:
            msg += " or by reacting to this message with ▶️."
            join_message = await ctx.channel.send(msg)
            session.message_join = join_message
            await join_message.add_reaction("▶️")
            return
        await ctx.channel.send(msg)

    #Join an existing game room by message.
    @tictactoe.command(aliases=["enter"])
    async def join(self, ctx, room_id=None):
        #In case of no room ID specified.
        if room_id == None:
            msg = "Please specify a room ID to join as `!ttt join XXXX`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Join room with specified room ID.
        await self.join_game(ctx.channel, self.game_sessions, room_id.upper(), ctx.author, self.max_players())

    #Quit a room.
    @tictactoe.command(aliases=["stop", "exit", "end", "leave"])
    async def quit(self, ctx, room_id=None):
        #In case of no room ID specified
        if room_id == None:
            msg = "Please specify a room ID to quit as `!ttt quit XXXX` or use `!ttt quit all`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return

        #Quit all rooms a player is in.
        if room_id.lower() in ["all", "every", "everything"]:
            rooms_quit = 0
            for session in reversed(self.game_sessions):
                if ctx.author in session.players:
                    await self.quit_game(self.game_sessions, session.room_id, ctx.author)
                    rooms_quit += 1
            msg = "An unknown error occurred."
            if rooms_quit == 0:
                msg = f"{ctx.author.name} is not in any rooms."
            else:
                msg = f"Removed {ctx.author.name} from {rooms_quit} room(s)."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return

        #Quit a specific room
        return_code = await self.quit_game(self.game_sessions, room_id.upper(), ctx.author)
        msg = "An unknown error occurred."
        if return_code == 0:
            msg = f"Removed {ctx.author.name} from room {room_id}."
        elif return_code == 1:
            msg = f"{ctx.author.name} is not in room {room_id}."
        elif return_code == 2:
            msg = f"Room {room_id} does not exist."
        await ctx.channel.send(content=msg, delete_after=15.0)

    #Reaction handling
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, player):
        #Prevent bot's own reactions triggering this
        if player == self.client.user:
            return
        for session in self.game_sessions:
            #Joining game by reacting with play emoji
            print(reaction.message.id)
            print(session.message_join.id)
            if reaction.message.id == session.message_join.id and reaction.emoji == "▶️":
                await self.join_game(reaction.message.channel, self.game_sessions, session.room_id, player, self.max_players())
                return

            #Taking turn by reacting with number emoji
            if session.message_board != None and reaction.message.id == session.message_board.id:
                if player.id == session.players[session.player_turn].id:
                    #Find which number was reacted with
                    pos = common.emoji_to_number(reaction.emoji)
                    if str(pos) in session.board_state:
                        await self.process_turn(session, pos, reaction)
                return

#Client Setup
def setup(client):
    client.add_cog(TictactoeCog(client))
