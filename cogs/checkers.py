#===============================================================================
# Checkers v1.2
# - Last Updated: 02 Jun 2021
#===============================================================================
# Update History
# ..............................................................................
# 02 Jun 2021 - Added support for inactivity timer of sessions. -YJ
# 26 May 2021 - Hastily rewrote some code to make parts of it extend base
#               classes. -YJ
# 22 May 2021 - File finished by RK. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Extend more base classes and clean up code. -YJ
#===============================================================================
# Description
# ..............................................................................
# checkers.py plays a game between two users on an 8x8 checkerboard. The first
# three rows on either side of the checkerboard are filled with tokens of either
# player. Tokens can move one diagonal space forwards each turn. An adjacent
# token can be eliminated by jumping over it. If an elimination move is possible
# it must be taken. When a token reaches the other side of the board, it is
# crowned and gains the ability to move backwards as well as move any number
# of spaces, as opposed to just one. The first player to eliminate all opponent
# tokens wins.
#===============================================================================

#Import Modules
import discord
from discord import Message, User
from discord.ext import commands

from common.session import Session
from common.player import Player
from common.game import Game
from common.emoji import number_to_emoji, emoji_to_number, string_to_emoji
from common.message import create_winner_message

from database import dbfunctions

from copy import copy, deepcopy
from abc import ABC, abstractmethod

#Checkers Session
class CheckersSession(Session):
    def __init__(self, parent):
        Session.__init__(self, parent)
        self.__message_board = None

    @property
    def message_board(self):
        return self.__message_board

    @message_board.setter
    def message_board(self, message_board: Message):
        self.__message_board = message_board

#Checkers Cog
class CheckersCog(Game):
    #Define variables.
    def __init__(self, client):
        Game.__init__(self, client)
        self.all_reactions = ["◀️","▶️","1️⃣","2️⃣","3️⃣", "4️⃣","➕"]
        self.moves = ["1","2","3","4"]
        self.current_tiles = []
        self.current = 0
        self.strikes = False
        self.value = ""
        self.player2 = ""
        self.player1 = ""
        self.old_board = [[Empty([0,0]),           Normal("Purple",[0,1]), Empty([0,2]),           Normal("Purple",[0,3]), Empty([0,4]),           Normal("Purple",[0,5]), Empty([0,6]),           Normal("Purple",[0,7])],
                          [Normal("Purple",[1,0]), Empty([1,1]),           Normal("Purple",[1,2]), Empty([1,3]),           Normal("Purple",[1,4]), Empty([1,5]),           Normal("Purple",[1,6]), Empty([1,7])],
                          [Empty([2,0]),           Normal("Purple",[2,1]), Empty([2,2]),           Normal("Purple",[2,3]), Empty([2,4]),           Normal("Purple",[2,5]), Empty([2,6]),           Normal("Purple",[2,7])],
                          [Empty([3,0]),           Empty([3,1]),           Empty([3,2]),           Empty([3,3]),           Empty([3,4]),           Empty([3,5]),           Empty([3,6]),           Empty([3,7])],
                          [Empty([4,0]),           Empty([4,1]),           Empty([4,2]),           Empty([4,3]),           Empty([4,4]),           Empty([4,5]),           Empty([4,6]),           Empty([4,7])],
                          [Normal("Green",[5,0]),  Empty([5,1]),           Normal("Green",[5,2]),  Empty([5,3]),           Normal("Green",[5,4]),  Empty([5,5]),           Normal("Green",[5,6]),  Empty([5,7])],
                          [Empty([6,0]),           Normal("Green",[6,1]),  Empty([6,2]),           Normal("Green",[6,3]),  Empty([6,4]),           Normal("Green",[6,5]),  Empty([6,6]),           Normal("Green",[6,7])],
                          [Normal("Green",[7,0]),  Empty([7,1]),           Normal("Green",[7,2]),  Empty([7,3]),           Normal("Green",[7,4]),  Empty([7,5]),           Normal("Green",[7,6]),  Empty([7,7])]]
        self.board = []
        self.instant_start = True
        self.game_name = "Checkers"
        self.game_abbrev = "ch"

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Checkers cog loaded.")

    #Game instructions
    def instructions(self):
        msg = "**Checkers Help**\n"
        msg += "Capture all opponent tokens! Your tokens can move one space diagonally each turn, or capture an adjacent opponent piece by jumping over it. If you can capture, you must. If a token reaches the end of the board, it gains the ability to move multiple spaces and move backwards.\n"
        msg += "`!ch new`: Start a new room.\n"
        msg += "`!ch join XXXX`: Join an existing room with its room ID specified in place of XXXX.\n"
        msg += "`!ch players XXXX`: Get a list of players in an existing room with its room ID specified in place of XXXX.\n"
        msg += "`!ch quit XXXX`: Quit a room you're in with its room ID specified in place of XXXX. The game continues if other players remain.\n"
        msg += "`!ch quit all`: Quit all rooms you're in. The games continue if other players remain."
        return msg

    #Board is now 8*8 which is standard
    def stones_left(self, board, value): #checks if one player has Checkers (to know who won check which move was done last)
        stones = 0
        for i in range(8):
            for j in range(8):
                if board[i][j].getColor() == value:
                    stones += 1
        return stones

    def strike_moves(self, board, value):
        tiles = []
        for i in range(8):
            for j in range(8):
                if board[i][j].getColor() == value:
                    if board[i][j].canStrike(board):
                        tiles.append(board[i][j])
        return tiles

    def normal_moves(self, board, value):
        tiles = []
        for i in range(8):
            for j in range(8):
                if board[i][j].getColor() == value:
                    if board[i][j].canMove(board):
                        tiles.append(board[i][j])
        return tiles

    def valid_board(self, board):
        for i in range(8):
            for j in range(8):
                if not isinstance(board[i][j],GameObject):
                    return False
        return True

    def remove_numbers(self, board):
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j],Empty):
                    board[i][j].setNumber(0)

    def number_to_coordinate(self, board, number):
        cc = [-1,-1] #will throw an out of bounds exception
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j],Empty):
                    if board[i][j].getNumber() == number:
                        cc = [i,j]
        return cc

    def emojis_on_board(self, board):
        tiles = []
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j],Empty):
                    if board[i][j].getNumber()==1:
                        tiles.append("1️⃣")
                    elif board[i][j].getNumber()==2:
                        tiles.append("2️⃣")
                    elif board[i][j].getNumber()==3:
                        tiles.append("3️⃣")
                    elif board[i][j].getNumber()==4:
                        tiles.append("4️⃣")
        return tiles


    def print_board(self, board, current):
        msg = ""
        if self.valid_board(board):
            for i in range(8):
                for j in range(8):
                    if current.getCoordinates() == [i,j]:
                        if isinstance(current, Dam):
                            msg += ":heart:"
                        else:
                            msg += ":red_circle:"
                    else:
                        msg += board[i][j].toString()
                msg += "\n"
            return msg
        else:
            return string_to_emoji("ERROR")

    def board_to_msg(self, board, value, current): # Translates the board data to a string
        msg = ""
        if value == "Green": #switch around the values when this message is called, because the players are not yet swapped
            msg = "It's your turn :green_circle:" + self.player1.user.mention + "!"
        else:
            msg = "It's your turn :purple_circle:" + self.player2.user.mention + "!"
        msg += "\n\nCurrent tile: :red_circle:\n\n" + self.print_board(board,current) + "\n\n\n"
        return msg

    #Setup the initial variables and message.
    async def setup_game(self, session, channel):
        await Game.setup_game(self, session, channel)
        session.shuffle_players()
        self.player1 = session.players[0]
        self.player2 = session.players[1]
        self.board = deepcopy(self.old_board)
        self.value = "Green"
        self.current_tiles = self.normal_moves(self.board, self.value)
        self.current = 0
        self.current_tiles[self.current].setMove(False,self.board)
        msg = self.board_to_msg(self.board, self.value, self.current_tiles[self.current])
        game_board = await channel.send(msg)
        session.message_board = game_board

        reaction = "◀️"
        await game_board.add_reaction(reaction)
        reaction = "▶️"
        await game_board.add_reaction(reaction)
        for i in range(4):
            reaction = number_to_emoji(i+1)
            await game_board.add_reaction(reaction)
        reaction = "➕"
        await game_board.add_reaction(reaction)

    #Handle additional checks required when a player quits the game.
    async def remove_player(self, session, user):
        session.remove_player(user)
        if session.message_board != None:
            await session.message_board.delete()
        self.game_sessions.remove(session)

    #Primary Functions
    #With no arguments specified, send game instructions.
    @commands.group(name="checkers", aliases=["ch", "chck", "checker", "draughts"], case_insensitive=True, invoke_without_command=True)
    async def checkers(self, ctx, *args):
        await ctx.channel.send(self.instructions())

    #Help command to receive instructions.
    @checkers.command(aliases=["?", "info", "information", "instructions"])
    async def help(self, ctx):
        await ctx.channel.send(self.instructions())

    #See the list of players of a room.
    @checkers.command(aliases=["player", "players", "playerlist", "playerslist", "players_list", "list"])
    async def player_list(self, ctx, room_id=None):
        await Game.player_list(self, ctx, room_id)

    #Register a new game room.
    @checkers.command(aliases=["start", "begin", "create", "register", "host"])
    async def new(self, ctx):
        session = CheckersSession(self)
        player = Player(ctx.author)
        await Game.new(self, ctx, session, player)

    #Join an existing game room by message.
    @checkers.command(aliases=["enter"])
    async def join(self, ctx, room_id=None):
        player = Player(ctx.author)
        await Game.join(self, ctx, room_id, player)

    #Quit a room.
    @checkers.command(aliases=["stop", "exit", "end", "leave"])
    async def quit(self, ctx, room_id=None):
        await Game.quit(self, ctx, room_id)


    #Play Checkers
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #Prevent bot's own reactions triggering this
        if user == self.client.user:
            return
        for session in self.game_sessions:
            #Joining game by reacting with play emoji
            if session.message_join != None and reaction.message.id == session.message_join.id and reaction.emoji == "▶️":
                ctx = await self.client.get_context(reaction.message)
                await Game.join(self, ctx, session.room_id, Player(user))
                return

        game_board = reaction.message
        player_id = user.id
        #Check if a reaction was posted to the message with the board
        for index, session in enumerate(self.game_sessions):
                            #remove new number reactions to make it more clear
            new_reaction = copy(reaction.emoji)
            if session.message_board != None and user != session.message_board.author and reaction.emoji in self.all_reactions:
                await game_board.remove_reaction(reaction.emoji,user)
            if session.message_board != None and player_id == session.players[0].user.id and game_board.id == session.message_board.id:
                if new_reaction in self.emojis_on_board(self.board):
                    new_pos = self.number_to_coordinate(self.board,emoji_to_number(new_reaction))
                    if not self.strikes: #other player has turn
                        self.current_tiles[self.current].doMove(False,new_pos,self.board)
                        self.remove_numbers(self.board)
                        if self.value == "Green":
                            self.value = "Purple"
                        else:
                            self.value = "Green"
                        session.players.append(session.players[0])  #end turn
                        del session.players[0]
                    else:
                        self.current_tiles[self.current].doMove(True,new_pos,self.board)
                        self.remove_numbers(self.board)
                        self.current_tiles.clear()
                        self.current_tiles.append(self.board[new_pos[0]][new_pos[1]])
                        self.current=0
                        if not self.current_tiles[0].canStrike(self.board):
                            if self.value == "Green":
                                self.value = "Purple"
                            else:
                                self.value = "Green"
                            session.players.append(session.players[0])  #end turn
                            del session.players[0]
                        else:
                            self.current_tiles[self.current].setMove(self.strikes,self.board)
                            msg = self.board_to_msg(self.board,self.value,self.current_tiles[self.current])
                            await game_board.edit(content=msg)
                            break
                    self.current = 0
                    self.current_tiles = self.strike_moves(self.board, self.value)
                    self.strikes = True
                    if len(self.current_tiles) == 0:
                        self.current_tiles = self.normal_moves(self.board, self.value)
                        self.strikes = False
                    if  len(self.current_tiles) > 0:
                        self.current_tiles[self.current].setMove(self.strikes,self.board)
                elif new_reaction in ["▶️","◀️"]:
                    if new_reaction == "▶️":
                        self.remove_numbers(self.board)
                        if (self.current + 1) < len(self.current_tiles):
                            self.current += 1
                        else:
                            self.current = 0
                    if new_reaction == "◀️":
                        self.remove_numbers(self.board)
                        if (self.current - 1) >= 0:
                            self.current = self.current - 1
                        else:
                            self.current = len(self.current_tiles) -1
                    if self.strikes:
                        self.current_tiles[self.current].setMove(True,self.board)
                    else:
                        self.current_tiles[self.current].setMove(False,self.board)
                elif new_reaction == "➕":
                    if self.current_tiles[self.current].isDam:
                        self.current_tiles[self.current].nextMultiplier(self.strikes)
                        self.remove_numbers(self.board)
                        if self.strikes:
                            self.current_tiles[self.current].setMove(True,self.board)
                        else:
                            self.current_tiles[self.current].setMove(False,self.board)
                if  len(self.current_tiles) >0:
                    msg = self.board_to_msg(self.board,self.value,self.current_tiles[self.current])
                if self.stones_left(self.board,"Green") == 0 or self.stones_left(self.board,"Purple") == 0:
                    msg = self.board_to_msg(self.board,self.value,Empty([-1,-1]))
                    winner = session.players[1].user
                    dbfunctions.boardgame_action("Checkers", winner.id, session.message_board, 'w')
                    loser = session.players[0].user
                    dbfunctions.boardgame_action("Checkers", loser.id, session.message_board, 'l')
                    msg += "\n\n" + winner.name + " has won the game!\n"
                session.inactivity_timer_restart()
                await game_board.edit(content=msg)



class GameObject(ABC):
    #all elements of the board
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def getCoordinates(self):
        return self.coordinates

    def setCoordinates(self, new):
        self.coordinates = new

    @abstractmethod
    def toString(self):
        pass

    @abstractmethod
    def getColor(self):
        pass

class Empty(GameObject):
    #empty places on the board

    def __init__(self, coordinates):
        GameObject.__init__(self, coordinates)
        self.number = 0
        self.empty_board = [["0","1","0","1","0","1","0","1"],["1","0","1","0","1","0","1","0"],["0","1","0","1","0","1","0","1"],["1","0","1","0","1","0","1","0"],["0","1","0","1","0","1","0","1"],["1","0","1","0","1","0","1","0"],["0","1","0","1","0","1","0","1"],["1","0","1","0","1","0","1","0"]]

    def setNumber(self, new_number):
        if new_number in [1,2,3,4]:
            self.number = new_number
        else:
            self.number = 0

    def getNumber(self):
        return self.number

    #override abstractmethod of GameObject
    def getColor(self):
        return "Empty"

    #override abstractmethod of GameObject
    def toString(self):
        if self.number in [1,2,3,4]:
            if self.number == 1:
                return ":one:"
            elif self.number == 2:
                return ":two:"
            elif self.number == 3:
                return ":three:"
            else:
                return ":four:"
        elif self.empty_board[self.coordinates[0]][self.coordinates[1]] == "1":
            return ":black_large_square:"
        else:
            return ":white_large_square:"


class Stone(GameObject,ABC):
    #all movable objects

    def __init__(self, dam, color, coordinates):
        self.color = color
        self.isDam = dam
        GameObject.__init__(self, coordinates)

    #override abstractmethod of GameObject
    def getColor(self):
        return self.color

    @abstractmethod
    def doMove(self,isStrike,place,board):
        pass

    @abstractmethod
    def setMove(self,isStrike,board):
        pass

    @abstractmethod
    def canStrike(self):
        pass

    @abstractmethod
    def canMove(self,board):
        pass

    #override abstractmethod of GameObject
    def toString(self):
        if not self.isDam:
            if self.color == "Green":
                return ":green_circle:"
            else:
                return ":purple_circle:"
        else:
            if self.color == "Green":
                return ":green_heart:"
            else:
                return ":purple_heart:"

class Normal(Stone):
    #A normal stone

    def __init__(self, color, coordinates):
        self.moves = []
        self.strikes = []
        Stone.__init__(self, False, color, coordinates)

    def doMove(self,isStrike,place,board):
        if isStrike:
            if place[0]>self.coordinates[0]:
                if place[1]>self.coordinates[1]:
                    board[place[0]-1][place[1]-1] = Empty([place[0]-1,place[1]-1])
                else:
                    board[place[0]-1][place[1]+1] = Empty([place[0]-1,place[1]+1])
            else:
                if place[1]>self.coordinates[1]:
                    board[place[0]+1][place[1]-1] = Empty([place[0]+1,place[1]-1])
                else:
                    board[place[0]+1][place[1]+1] = Empty([place[0]+1,place[1]+1])
        if self.color == "Green":
            if place[0]==0:
                board[place[0]][place[1]] = Dam(self.color,place)
            else:
                board[place[0]][place[1]] = Normal(self.color,place)
        else:
            if place[0]==7:
                board[place[0]][place[1]] = Dam(self.color,place)
            else:
                board[place[0]][place[1]] = Normal(self.color,place)

        board[self.coordinates[0]][self.coordinates[1]] = Empty(self.coordinates)

    def setMove(self,isStrike,board):
        if isStrike:
            for i in range(len(self.strikes)):
                board[self.strikes[i][0]][self.strikes[i][1]].setNumber(i+1)
        else:
            for i in range(len(self.moves)):
                board[self.moves[i][0]][self.moves[i][1]].setNumber(i+1)

    def canStrike(self,board):
        tiles = []
        counter = 0
        opposite = "Green"
        if self.color == "Green":
            opposite = "Purple"
        if self.coordinates[0]>1 and self.coordinates[1]>1:#not in top left
            if board[self.coordinates[0]-1][self.coordinates[1]-1].getColor() == opposite:
                if board[self.coordinates[0]-2][self.coordinates[1]-2].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]-2][self.coordinates[1]-2].getCoordinates())
                    counter += 1
        if self.coordinates[0]>1 and self.coordinates[1]<6:#not in top left
            if board[self.coordinates[0]-1][self.coordinates[1]+1].getColor() == opposite:
                if board[self.coordinates[0]-2][self.coordinates[1]+2].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]-2][self.coordinates[1]+2].getCoordinates())
                    counter += 1
        if self.coordinates[0]<6 and self.coordinates[1]>1:#not in top left
            if board[self.coordinates[0]+1][self.coordinates[1]-1].getColor() == opposite:
                if board[self.coordinates[0]+2][self.coordinates[1]-2].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]+2][self.coordinates[1]-2].getCoordinates())
                    counter += 1
        if self.coordinates[0]<6 and self.coordinates[1]<6:#not in top left
            if board[self.coordinates[0]+1][self.coordinates[1]+1].getColor() == opposite:
                if board[self.coordinates[0]+2][self.coordinates[1]+2].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]+2][self.coordinates[1]+2].getCoordinates())
                    counter += 1
        self.strikes = tiles
        return counter > 0

    def canMove(self,board):
        tiles = []
        counter = 0
        if self.color == "Green":
            if self.coordinates[0]>0 and self.coordinates[1]>0:#not in top left
                if board[self.coordinates[0]-1][self.coordinates[1]-1].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]-1][self.coordinates[1]-1].getCoordinates())
                    counter += 1
            if self.coordinates[0]>0 and self.coordinates[1]<7:#not in top right
                if board[self.coordinates[0]-1][self.coordinates[1]+1].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]-1][self.coordinates[1]+1].getCoordinates())
                    counter += 1
        else:
            if self.coordinates[0]<7 and self.coordinates[1]>0:#not in top left
                if board[self.coordinates[0]+1][self.coordinates[1]-1].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]+1][self.coordinates[1]-1].getCoordinates())
                    counter += 1
            if self.coordinates[0]<7 and self.coordinates[1]<7:#not in top right
                if board[self.coordinates[0]+1][self.coordinates[1]+1].getColor() == "Empty":
                    tiles.append(board[self.coordinates[0]+1][self.coordinates[1]+1].getCoordinates())
                    counter += 1
        self.moves = tiles
        return counter > 0


class Dam(Stone):
    # a dam.

    def __init__(self, color, coordinates):
        Stone.__init__(self, True, color, coordinates)
        self.current = 0
        self.moveMultipliers = []
        self.strikeMultipliers = []

    def doMove(self,isStrike,place,board):
        opposite = "Green"
        if self.color == "Green":
            opposite = "Purple"
        if isStrike:
            if place[0]>self.coordinates[0]:
                if place[1]>self.coordinates[1]:
                    for i in range(place[0]-self.coordinates[0]-1):
                        if board[place[0]-1-i][place[1]-1-i].getColor() == opposite:
                            board[place[0]-1-i][place[1]-1-i] = Empty([place[0]-1-i,place[1]-1-i])
                else:
                    for i in range(place[0]-self.coordinates[0]-1):
                        if board[place[0]-1-i][place[1]+1+i].getColor() == opposite:
                            board[place[0]-1-i][place[1]+1+i] = Empty([place[0]-1-i,place[1]+1+i])
            else:
                if place[1]>self.coordinates[1]:
                    for i in range(self.coordinates[0]-place[0]-1):
                        if board[place[0]+1+i][place[1]-1-i].getColor() == opposite:
                            board[place[0]+1+i][place[1]-1-i] = Empty([place[0]+1+i,place[1]-1-i])
                else:
                    for i in range(self.coordinates[0]-place[0]-1):
                        if board[place[0]+1+i][place[1]+1+i].getColor() == opposite:
                            board[place[0]+1+i][place[1]+1+i] = Empty([place[0]+1+i,place[1]+1+i])
        board[place[0]][place[1]] = Dam(self.color,place)
        board[self.coordinates[0]][self.coordinates[1]] = Empty(self.coordinates)


    def setMove(self,isStrike,board):
        if isStrike:
            strikes = self.findStrikes(self.current,board)
            for i in range(len(strikes)):
                board[strikes[i][0]][strikes[i][1]].setNumber(i+1)
        else:
            moves = self.findMoves(self.current,board)
            for i in range(len(moves)):
                board[moves[i][0]][moves[i][1]].setNumber(i+1)

    def canStrike(self,board):
        self.setStrikeMultipliers(board)
        if (len(self.strikeMultipliers) > 0):
            self.current = self.strikeMultipliers[0]
            return True
        return False


    def canMove(self,board):
        self.setMoveMultipliers(board)
        if (len(self.moveMultipliers) > 0):
            self.current = self.moveMultipliers[0]
            return True
        return False

    def setMoveMultipliers(self,board):
        multipliers = []
        for i in range(7):
            tiles = self.findMoves(i,board)
            if len(tiles) > 0:
                multipliers.append(i)
        self.moveMultipliers = multipliers

    def setStrikeMultipliers(self,board):
        multipliers = []
        for i in range(7):
            tiles = self.findStrikes(i,board)
            if len(tiles) > 0:
                multipliers.append(i)
        self.strikeMultipliers = multipliers


    def findMoves(self,multiplier,board):
        tiles = []
        counter = 0
        empty = True
        if self.coordinates[0]>multiplier and self.coordinates[1]>multiplier:#not in top left
            a = multiplier
            while(a>=0):
                if not board[self.coordinates[0]-(1+a)][self.coordinates[1]-(1+a)].getColor() == "Empty":
                    empty = False
                    break
                a=a-1
            if(empty):
                tiles.append(board[self.coordinates[0]-(1+multiplier)][self.coordinates[1]-(1+multiplier)].getCoordinates())
            else:
                empty = True
        if self.coordinates[0]>multiplier and self.coordinates[1]<(7-multiplier):#not in top right
            a = multiplier
            while(a>=0):
                if not board[self.coordinates[0]-(1+a)][self.coordinates[1]+(1+a)].getColor() == "Empty":
                    empty = False
                    break
                a=a-1
            if(empty):
                tiles.append(board[self.coordinates[0]-(1+multiplier)][self.coordinates[1]+(1+multiplier)].getCoordinates())
            else:
                empty = True
        if self.coordinates[0]<(7-multiplier) and self.coordinates[1]>multiplier:#not in top left
            a = multiplier
            while(a>=0):
                if not board[self.coordinates[0]+(1+a)][self.coordinates[1]-(1+a)].getColor() == "Empty":
                    empty = False
                    break
                a=a-1
            if(empty):
                tiles.append(board[self.coordinates[0]+(1+multiplier)][self.coordinates[1]-(1+multiplier)].getCoordinates())
            else:
                empty = True
        if self.coordinates[0]<(7-multiplier) and self.coordinates[1]<(7-multiplier):#not in top right
            a = multiplier
            while(a>=0):
                if not board[self.coordinates[0]+(1+a)][self.coordinates[1]+(1+a)].getColor() == "Empty":
                    empty = False
                    break
                a=a-1
            if(empty):
                tiles.append(board[self.coordinates[0]+(1+multiplier)][self.coordinates[1]+(1+multiplier)].getCoordinates())
            else:
                empty = True
        return tiles

    def findStrikes(self,multiplier,board):
        tiles = []
        opposite = "Green"
        if self.color == "Green":
            opposite = "Purple"
        empty = True
        if self.coordinates[0]>multiplier+1 and self.coordinates[1]>multiplier+1:#not in top left
            if board[self.coordinates[0]-(2+multiplier)][self.coordinates[1]-(2+multiplier)].getColor() == "Empty":
                b = 0
                a = multiplier
                while(a>=0):
                    if b>0:
                        if not board[self.coordinates[0]-(1+a)][self.coordinates[1]-(1+a)].getColor() == "Empty":
                            empty = False
                            break
                    if board[self.coordinates[0]-(1+a)][self.coordinates[1]-(1+a)].getColor() == opposite:
                        b+=1
                    elif not board[self.coordinates[0]-(1+a)][self.coordinates[1]-(1+a)].getColor() == "Empty":
                        empty = False
                        break
                    a=a-1
                if(empty and b>0):
                    tiles.append(board[self.coordinates[0]-(2+multiplier)][self.coordinates[1]-(2+multiplier)].getCoordinates())
                else:
                    empty = True
        if self.coordinates[0]>multiplier+1 and self.coordinates[1]<(6-multiplier):#not in top right
            if board[self.coordinates[0]-(2+multiplier)][self.coordinates[1]+(2+multiplier)].getColor() == "Empty":
                b = 0
                a = multiplier
                while(a>=0):
                    if b>0:
                        if not board[self.coordinates[0]-(1+a)][self.coordinates[1]+(1+a)].getColor() == "Empty":
                            empty = False
                            break
                    if board[self.coordinates[0]-(1+a)][self.coordinates[1]+(1+a)].getColor() == opposite:
                        b+=1
                    elif not board[self.coordinates[0]-(1+a)][self.coordinates[1]+(1+a)].getColor() == "Empty":
                        empty = False
                        break
                    a=a-1
                if(empty and b>0):
                    tiles.append(board[self.coordinates[0]-(2+multiplier)][self.coordinates[1]+(2+multiplier)].getCoordinates())
                else:
                    empty = True
        if self.coordinates[0]<(6-multiplier) and self.coordinates[1]>multiplier+1:#not in top left
            if board[self.coordinates[0]+(2+multiplier)][self.coordinates[1]-(2+multiplier)].getColor() == "Empty":
                b = 0
                a = multiplier
                while(a>=0):
                    if b>0:
                        if not board[self.coordinates[0]+(1+a)][self.coordinates[1]-(1+a)].getColor() == "Empty":
                            empty = False
                            break
                    if board[self.coordinates[0]+(1+a)][self.coordinates[1]-(1+a)].getColor() == opposite:
                        b+=1
                    elif not board[self.coordinates[0]+(1+a)][self.coordinates[1]-(1+a)].getColor() == "Empty":
                        empty = False
                        break
                    a=a-1
                if(empty and b>0):
                    tiles.append(board[self.coordinates[0]+(2+multiplier)][self.coordinates[1]-(2+multiplier)].getCoordinates())
                else:
                    empty = True
        if self.coordinates[0]<(6-multiplier) and self.coordinates[1]<(6-multiplier):#not in top right
            if board[self.coordinates[0]+(2+multiplier)][self.coordinates[1]+(2+multiplier)].getColor() == "Empty":
                b = 0
                a = multiplier
                while(a>=0):
                    if b>0:
                        if not board[self.coordinates[0]+(1+a)][self.coordinates[1]+(1+a)].getColor() == "Empty":
                            empty = False
                            break
                    if board[self.coordinates[0]+(1+a)][self.coordinates[1]+(1+a)].getColor() == opposite:
                        b+=1
                    elif not board[self.coordinates[0]+(1+a)][self.coordinates[1]+(1+a)].getColor() == "Empty":
                        empty = False
                        break
                    a=a-1
                if(empty and b>0):
                    tiles.append(board[self.coordinates[0]+(2+multiplier)][self.coordinates[1]+(2+multiplier)].getCoordinates())
                else:
                    empty = True
        return tiles

    def nextMultiplier(self,isStrike):
        if isStrike:
            if (self.strikeMultipliers.index(self.current)+1)<len(self.strikeMultipliers):
                self.current = self.strikeMultipliers[self.strikeMultipliers.index(self.current)+1]
            else:
                self.current = self.strikeMultipliers[0]
        else:
            if (self.moveMultipliers.index(self.current)+1)<len(self.moveMultipliers):
                self.current = self.moveMultipliers[self.moveMultipliers.index(self.current)+1]
            else:
                self.current = self.moveMultipliers[0]

    def toString(self):
        if self.color == "Green":
            return ":green_heart:"
        else:
            return ":purple_heart:"






#Client Setup
def setup(client):
    client.add_cog(CheckersCog(client))
