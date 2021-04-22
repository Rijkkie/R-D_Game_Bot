#===============================================================================
# fourOnARow v1.0
# - Last Updated: 22 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 22 Apr 2021 - Trial and errored until it worked -RK
# 21 Apr 2021 - Started file. copied yoris code lol -RK
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
# tictactoe.py plays a game where two players take turns choosing one of nine
# tiles to place their respective tokens. If three tiles in a row hold the same
# player's token, that player wins the game.
#===============================================================================

#Import Modules
from copy import copy, deepcopy # I imported this as well !!!!!
import discord
from discord.ext import commands
import common
import random

#Cog Setup
class fourOnARow(commands.Cog):
    #Define variables.
    def __init__(self, client):
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
                    if( not (board[i][j]=="0" or board[i][j]=="1" or board[i][j]=="2")):
                        return False
            return True
        else:
            return False

    def count_turns(self,board,value):
        counter = 0
        if(value =="1" or value == "2" ):
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
                    if board_state[i][j] == "1" or board_state[i][j] == "2":
                        token = board_state[i][j]
                        if token == board_state[i][j+1] and token == board_state[i][j+2] and token == board_state[i][j+3]:
                            return True
            #Check for vertical wins
            for j in range(7):
                for i in range(3):
                    if board_state[i][j] == "1" or board_state[i][j] == "2":
                        token = board_state[i][j]
                        if token == board_state[i+1][j] and token == board_state[i+2][j] and token == board_state[i+3][j]:
                            return True
            #Check for diagonal wins left to right
            for j in range(4):
                for i in range(3):
                    if board_state[i][j] == "1" or board_state[i][j] == "2":
                        token = board_state[i][j]
                        if token == board_state[i+1][j+1] and token == board_state[i+2][j+2] and token == board_state[i+3][j+3]:
                            return True
            #Check for diagonal wins right to left
            for j in range(4):
                j += 3
                for i in range(3):
                    if board_state[i][j] == "1" or board_state[i][j] == "2":
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
            #msg = "column is full."     Here needs to be a message that the column is full if possible/ otherwise check in on_reaction_add if column is full(maybe delete a reaction from numbers as well)
            #await ctx.message.channel.send(msg)
            return board


    def board_to_msg(self,board): # Translates the board data to a string
        msg = ":red_circle::"+self.player1.mention+"\n:yellow_circle::" +self.player2.mention +"\n\n|:one:|:two:|:three:|:four:|:five:|:six:|:seven:|\n\n"
        zero = ":black_medium_square:|"
        one = ":yellow_circle:|"
        two = ":red_circle:|"
        if(self.valid_board(board)):
            for i in range(6):
                msg+="|"
                for j in range(7):
                    if(board[i][j]=="0"):
                        msg += zero
                    elif(board[i][j]=="1"):
                        msg += one
                    else:
                        msg += two
                msg += "\n"
            return msg
        else:
            return "Shit there seems to be the problem with the board"

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
                                msg = self.board_to_msg(self.board)
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
            if player_id == session[2][0] and game_board.id == session[1].id:
                #Check if emoji is a number emoji and not replaced by token yet
                msg = game_board.content
                numbers = []
                for i in range(7):
                    if str(i+1) in session[3]:
                        numbers.append(common.number_to_emoji(i+1))
                if reaction.emoji in numbers:
                    #Find where to put the token, and which token to place
                    for i in range(7):
                        if reaction.emoji == common.number_to_emoji(i+1):
                            value = "1"
                            if ((self.count_turns(self.board,"1") + self.count_turns(self.board,"2")) % 2 == 0):
                                value = "2"
                            full_c= self.fullColumns #Kan beter dit
                            for c in range(7):
                                if(self.column_is_full(c, self.board)):
                                    full_c += 1
                            if(full_c>self.fullColumns):
                                self.fullColumns = full_c
                                session[2].append(session[2][0])
                                del session[2][0]
                            self.board = self.make_next_move(i,self.board,value)
                            msg = self.board_to_msg(self.board)
                            break  #maybe problems here when multiple reactions are pressed


                    #numpos = session[3].find(str(common.emoji_to_number(reaction.emoji)))
                    #token = ":yellow_circle:"
                    #char = "o"
                    #if (session[3].count("x") + session[3].count("o")) % 2 == 0:
                    #    token = ":red_circle:"
                    #    char = "x"
                    #msg = msg[:emojipos] + token + msg[emojipos+3:]
                    #Check if game is won, cycle turn to other player if not
                    if self.is_game_won(self.board) == True:
                        winner = await self.client.fetch_user(session[2][0])
                        msg += f"\n{winner.mention} has won the game!"
                        del self.game_sessions[index]
                    else:
                        session[2].append(session[2][0])
                        del session[2][0]
                    await game_board.edit(content=msg)

#Client Setup
def setup(client):
    client.add_cog(fourOnARow(client))
