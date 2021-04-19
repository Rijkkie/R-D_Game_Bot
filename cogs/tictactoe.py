#===============================================================================
# Tic-tac-toe v1.0
# - Last Updated: 19 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 19 Apr 2021 - Hacked together some gameplay code. Finished file -YJ
# 18 Apr 2021 - Started file. Made room creation code. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Add an expiry timer on that room ID or something, to prevent users from just
#   starting a bunch of empty rooms and hogging all the IDs. -YJ
# - Should probably clean this up and make it more functional sometime. -YJ
#===============================================================================
# Description
# ..............................................................................
# tictactoe.py plays a game where two players take turns choosing one of nine
# tiles to place their respective tokens. If three tiles in a row hold the same
# player's token, that player wins the game.
#===============================================================================

#Import Modules
import discord
from discord.ext import commands
import common
import random

#Cog Setup
class Tictactoe(commands.Cog):
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

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Tic-tac-toe cog loaded.")

    #Game instructions
    def help(self):
        return "**Tic-tac-toe!**\nStart with `!ttt new`\nJoin with `!ttt join`"

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

    #Set up tic-tac-toe.
    @commands.command(aliases=["ttt", "tic-tac-toe"])
    async def tictactoe(self, ctx, *args):
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
                msg = "New tic-tac-toe room created! Your room ID is: "
                msg += f"{room_id}.\nJoin by typing `!ttt join {room_id}`"
                await ctx.message.channel.send(msg)

            #Join an existing game room
            elif arg0 == "join":
                #In case of no room ID specified
                if len(args) < 2:
                    msg = "Please specify a room ID to join as `!ttt join XXXX`"
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
                                msg = "❌: " + self.client.get_user(session[2][0]).mention
                                msg += "\n⭕: " + self.client.get_user(session[2][1]).mention
                                msg += "\n\n1️⃣2️⃣3️⃣\n4️⃣5️⃣6️⃣\n7️⃣8️⃣9️⃣"
                                game_board = await ctx.message.channel.send(msg)
                                session[1] = game_board
                                for i in range(9):
                                    reaction = common.number_to_emoji(i+1)
                                    await game_board.add_reaction(reaction)
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

    #Play tic-tac-toe
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
                for i in range(9):
                    if str(i+1) in session[3]:
                        numbers.append(common.number_to_emoji(i+1))
                if reaction.emoji in numbers:
                    #Find where to put the token, and which token to place
                    emojipos = msg.rfind(reaction.emoji)
                    numpos = session[3].find(str(common.emoji_to_number(reaction.emoji)))
                    token = "⭕"
                    char = "o"
                    if (session[3].count("x") + session[3].count("o")) % 2 == 0:
                        token = "❌"
                        char = "x"
                    msg = msg[:emojipos] + token + msg[emojipos+3:]
                    session[3] = session[3][:numpos] + char + session[3][numpos+1:]
                    #Check if game is won, cycle turn to other player if not
                    if self.is_game_won(session[3]) == True:
                        winner = self.client.get_user(session[2][0]).mention
                        msg += f"\n{winner} has won the game!"
                        del self.game_sessions[index]
                    else:
                        session[2].append(session[2][0])
                        del session[2][0]
                    await game_board.edit(content=msg)

#Client Setup
def setup(client):
    client.add_cog(Tictactoe(client))
