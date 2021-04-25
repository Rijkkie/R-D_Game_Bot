#===============================================================================
# fourOnARow v1.0
# - Last Updated: 24 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 24 Apr 2021 - Added color and name of player that can make a move - RK
# 24 Apr 2021 - Fixed bug where when one column was filled only one player could
# play - RK
# 22 Apr 2021 - Game works for most cases -RK
# 21 Apr 2021 - Copied parts of tictactoe.py and started to think about
# what needed to be different -RK
#===============================================================================
# Notes
# ..............................................................................
# - Reset reactions after move-RK
# - SOMTHING THAT SHOWS Who can make a move(color) -RK
# - Make the game able to have different board sizes, different color styles-
#  (its now made for darkmode )-RK
# - Nothing is implemented for ties -RK
# - Should probably clean this up and make it more functional sometime. -YJ
#===============================================================================
# Description
# ..............................................................................
#===============================================================================

#Import Modules
from copy import copy, deepcopy # I imported this as well !!!!!
import discord
from discord.ext import commands
import common
import random
import time

#Cog Setup
class fourOnARow(commands.Cog):
    #Define variables.
    def __init__(self, client):
        self.all_numbers = ["0️⃣","1️⃣","2️⃣","3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        self.client = client
        self.game_sessions = [] #Array holding sessions, structured like this:
                                #> game_sessions
                                # L> session
                                #   L> room_id
                                #   L> message
                                #   L> players
                                #     L> player1_id
                                #     L> player2_id
                                #   L> board_state
                                # L> session
                                #etc.
        self.fullColumns = 0
        self.player2 = ""
        self.player1 = ""
        self.old_board = [["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"]]
        self.board = [["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"], ["0","0","0","0","0","0","0"]]
        #board kan dus weg als variable bij sommige functies

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("fourOnARow cog loaded.")

    #Game instructions
    def help(self):
        return "**fourOnARow!**\nStart with `!4row new`\nJoin with `!4row join`"

    #Check board state for a winning position
    #Board is now 6*7 which is standard


    def valid_board(self,board): #checks if the board is 6x7 and consists of only 0s, 1s and 2s
        if(len(board)==6):
            for i in range(6):
                if(len(board[i])!=7):
                    return False
                for j in range(7):
                    if( not (board[i][j]=="0" or board[i][j]=="Yellow" or board[i][j]=="Red")):
                        return False
            return True
        else:
            return False

    def count_turns(self,board,value):
        counter = 0
        if(value =="Yellow" or value == "Red" ):
            for i in range(6):
                for j in range(7):
                    if(board[i][j]==value):
                        counter+=1
        return counter



    def is_game_won(self, board_state): #checks if one player has 4 on a row (to know who won check which move was done last)
        if self.valid_board(board_state):
            #Check for horizontal wins (starting from x = 0 to x = 3 going x = 3 to x = 6)
            for i in range(6):
                for j in range(4):
                    if board_state[i][j] == "Yellow" or board_state[i][j] == "Red":
                        token = board_state[i][j]
                        if token == board_state[i][j+1] and token == board_state[i][j+2] and token == board_state[i][j+3]:
                            return True
            #Check for vertical wins
            for j in range(7):
                for i in range(3):
                    if board_state[i][j] == "Yellow" or board_state[i][j] == "Red":
                        token = board_state[i][j]
                        if token == board_state[i+1][j] and token == board_state[i+2][j] and token == board_state[i+3][j]:
                            return True
            #Check for diagonal wins left to right
            for j in range(4):
                for i in range(3):
                    if board_state[i][j] == "Yellow" or board_state[i][j] == "Red":
                        token = board_state[i][j]
                        if token == board_state[i+1][j+1] and token == board_state[i+2][j+2] and token == board_state[i+3][j+3]:
                            return True
            #Check for diagonal wins right to left
            for j in range(4):
                j += 3
                for i in range(3):
                    if board_state[i][j] == "Yellow" or board_state[i][j] == "Red":
                        token = board_state[i][j]
                        if token == board_state[i+1][j-1] and token == board_state[i+2][j-2] and token == board_state[i+3][j-3]:
                            return True


    def column_is_full(self,column, board): #checks if a column is full
        if(column<=7 and column >= 1 and self.valid_board(board)):
            for i in range(6):
                if board[i][column]=="0" :
                    return False
            return True
        else:
            return False

    def make_next_move(self,column, board, value): #checks if a move is possible and changes the board according to this move
        if( not (self.column_is_full(column, board))):
            for i in range(6):
                if(board[5-i][column]=="0"):
                    new_board = board
                    new_board[5-i][column] = value
                    return new_board
        else:
            return board

    def print_board(self,board,value):
        msg = ""
        zero = ":black_medium_square:|"
        yellow = ":yellow_circle:|"
        red = ":red_circle:|"
        if self.valid_board(board) and (value =="Yellow" or value == "Red"):
            for i in range(6):
                msg+="|"
                for j in range(7):
                    if(board[i][j]=="0"):
                        msg += zero
                    elif(board[i][j]=="Yellow"):
                        msg += yellow
                    else:
                        msg += red
                msg += "\n"
            return msg
        else:
            return common.string_to_emoji("ERROR")






    def board_to_msg(self,board,value): # Translates the board data to a string
        if value == "Yellow": #switch around the values when this message is called, because the players are not yet swapped
            msg = "It's your turn :red_circle::"+self.player1.mention + "!"
        else:
            msg = "It's your turn :yellow_circle::" +self.player2.mention + "!"
        msg += "\n\n|:one:|:two:|:three:|:four:|:five:|:six:|:seven:|\n\n" + self.print_board(board,value)
        return msg
    #Set up tic-tac-toe.
    @commands.command(aliases=["4row", "four_on_a_Row"])
    async def fouronarow(self, ctx, *args):
        #Check arguments specified with command message
        if len(args) < 1:
            #With no arguments specified, send game instructions
            await ctx.message.channel.send(self.help())
        else:
            arg0 = args[0]
            #Register a new game room
            if arg0 == "new":
                player_id = ctx.author.id
                room_id = common.generate_room_id(self.game_sessions)
                #Save new session
                session = [room_id, None, [player_id], "123456789"]
                self.game_sessions.append(session)
                #Send session's room ID
                msg = "New 4 on a row room created! Your room ID is: "
                msg += f"{room_id}.\nJoin by typing `!4row join {room_id}`"
                await ctx.message.channel.send(msg)

            #Join an existing game room
            elif arg0 == "join":
                #In case of no room ID specified
                if len(args) < 2:
                    msg = "Please specify a room ID to join as `!4row join XXXX`"
                    await ctx.message.channel.send(msg)
                #Join room with specified room ID
                else:
                    room_id = args[1].upper()
                    player_id = ctx.author.id
                    max_players = 2
                    return_code = common.join_room(self.game_sessions, room_id, player_id, max_players)
                    msg = "An unknown error occurred."
                    if return_code == 0:
                        for session in self.game_sessions:
                            if session[0] == room_id:
                                random.shuffle(session[2])
                                self.player1 = await self.client.fetch_user(session[2][0])
                                self.player2 = await self.client.fetch_user(session[2][1])
                                self.board = deepcopy(self.old_board)
                                msg = self.board_to_msg(self.board,"Yellow")
                                game_board = await ctx.message.channel.send(msg)
                                session[1] = game_board
                                for i in range(7):
                                    reaction = common.number_to_emoji(i+1)
                                    await game_board.add_reaction(reaction)
                    #onbelangrijk voor nu
                    elif return_code == 1:
                        player_name = ctx.author.name
                        msg = f"{player_name} is already in room {room_id}!"
                        await ctx.message.channel.send(msg)
                    elif return_code == 2:
                        msg = f"Room {room_id} is full."
                        await ctx.message.channel.send(msg)
                    elif return_code == 3:
                        msg = f"Room {room_id} does not exist."
                        await ctx.message.channel.send(msg)

    #Play fourOnARow
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        game_board = reaction.message
        player_id = user.id
        #Check if a reaction was posted to the message with the board
        for index, session in enumerate(self.game_sessions):
                            #remove new number reactions to make it more clear
            new_reaction = copy(reaction.emoji)
            if user != session[1].author and reaction.emoji in self.all_numbers:
                await game_board.remove_reaction(reaction.emoji,user)
            if player_id == session[2][0] and game_board.id == session[1].id:
                #Check if emoji is a number emoji and not replaced by token yet
                numbers = [] #Fill numbers with current reactions and delete unnecessary reactions
                for i in range(7):
                    if not self.column_is_full(i, self.board):
                        numbers.append(common.number_to_emoji(i+1))
                if new_reaction in numbers:
                    #Find where to put the token, and which token to place
                    for i in range(7):
                        if reaction.emoji == common.number_to_emoji(i+1):
                            value = "Yellow" # check which player is currently making a move
                            if ((self.count_turns(self.board,"Yellow") + self.count_turns(self.board,"Red")) % 2 == 0):
                                value = "Red"
                            self.board = self.make_next_move(i,self.board,value)
                            if self.column_is_full(i,self.board):
                                await game_board.clear_reaction(common.number_to_emoji(i+1)) #Remove number of column that is full
                            msg = self.board_to_msg(self.board,value)
                            break

                    if self.is_game_won(self.board) == True: # check if game is won by a player
                        winner = await self.client.fetch_user(session[2][0])
                        await game_board.edit(content=msg)
                        for i in numbers:
                            await game_board.clear_reaction(i)
                        time.sleep(1)
                        msg = self.board_to_msg(self.board,value) + "\n\n" + common.create_winner_message(winner.name)
                        del self.game_sessions[index]
                    else:
                        session[2].append(session[2][0])  #end turn
                        del session[2][0]
                    await game_board.edit(content=msg)


#Client Setup
def setup(client):
    client.add_cog(fourOnARow(client))
