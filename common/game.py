#===============================================================================
# Game v1.0
# - Last Updated: 23 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 25 May 2021 - Added add_player to support checks on player join. -YJ
# 23 May 2021 - Started and finished file. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - It's kind of a pain to have to specify the room_id for every command. Check
#   if a player is in just one room, and if they are, assume they are using a
#   command for that room specifically.
# - Quite a bit of code duplication between set_max_players and set_max_rounds.
#   Figure out how to generalize them. -YJ
#===============================================================================
# Description
# ..............................................................................
# game.py contains the Game class, used for most general features shared across
# the bot's games.
#===============================================================================

#Import Modules
import discord
from discord import Message, User
from discord.ext import commands

from common.session import Session
from common.player import Player
from common.card import Card

import random
import math

#Cog Class
class Game(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.game_sessions = []
        self.instant_start = False
        self.game_name = "Game"
        self.game_abbrev = "game"

    #Get maximum amount of players of a session. Override if needed.
    def get_max_players(self, session):
        return 0

    #Get minimum amount of players of a session. Override if needed.
    def get_min_players(self, session):
        return 0

    #Check whether a game has started yet. Override if needed.
    def has_game_started(self, session):
        return False

    #Setup the initial variables and message(s) of the game. Override if needed.
    async def setup_game(self):
        pass

    #Handle additional checks required when a player joins the game. Override if needed.
    async def add_player(self, session, user):
        session.add_player(user)

    #Handle additional checks required when a player quits the game. Override if needed.
    async def remove_player(self, session, user):
        session.remove_player(user)

    #Return the names of users in a game room.
    async def player_list(self, ctx, room_id):
        #In case of no room ID specified.
        if room_id == None:
            msg = f"Please specify a room ID to see its players as `!{self.game_abbrev} players XXXX`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Return player list of specified room.
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                msg = f"**{self.game_name} Room {session.room_id} Players:** "
                for i, player in enumerate(session.players):
                    if i:
                        msg += ", "
                    msg += f"{player.user.name}"
                await ctx.channel.send(msg)
                return
        msg = f"{self.game_name} room {room_id} not found."
        await ctx.channel.send(msg)

    #Register a new game room.
    async def new(self, ctx, session, player):
        await self.add_player(session, player)
        self.game_sessions.append(session)
        #Send session's room ID
        msg = f"New {self.game_name} room created! Your room ID is: {session.room_id}.\n"
        if self.instant_start == False:
            msg += f"The game can be started typing `!{self.game_abbrev} start {session.room_id}`\n"
        msg += f"Others can join by typing `!{self.game_abbrev} join {session.room_id}`"
        if ctx.guild != None:
            msg += " or by reacting to this message with ▶️."
            join_message = await ctx.channel.send(msg)
            session.message_join = join_message
            await join_message.add_reaction("▶️")
            return
        await ctx.channel.send(msg)

    #Join an existing game room.
    async def join(self, ctx, room_id, player):
        #In case of joining through DMs.
        if ctx.guild == None and self.instant_start == True:
            msg = "Please join the game in a public channel."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #In case of no room ID specified.
        if room_id == None:
            msg = f"Please specify a room ID to join as `!{self.game_abbrev} join XXXX`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Attempt to join room.
        msg = f"{self.game_name} room {room_id} does not exist."
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                #Check if player is already in room
                if any(active_player.user.id == player.user.id for active_player in session.players):
                    msg = f"{player.user.name} is already in {self.game_name} room {session.room_id}!"
                    break
                #Check if room is full
                max_players = self.get_max_players(session)
                if max_players > 0 and len(session.players) >= max_players:
                    msg = f"{self.game_name} room {session.room_id} is full."
                    break
                #Add player to room
                await self.add_player(session, player)
                if self.instant_start == True:
                    await self.setup_game(session, ctx.channel)
                    return
                msg = f"{player.user.name} joined {self.game_name} room {session.room_id}!"
                await ctx.channel.send(msg)
                return
        await ctx.channel.send(content=msg, delete_after=15.0)

    #Start a game.
    async def start(self, ctx, room_id):
        #In case of trying to start game in DMs.
        if self.instant_start == True:
            msg = f"{self.game_name} starts automatically when enough players join."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        if ctx.guild == None:
            msg = "Please start the game in a public channel."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #In case of no room ID specified.
        if room_id == None:
            msg = f"Please specify a room ID to start its game as `!{self.game_abbrev} start XXXX`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Start game in specified room ID.
        msg = f"{self.game_name} room {room_id} not found."
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                #Check if player is in room
                if any(ctx.author.id == player.user.id for player in session.players):
                    #Check if room has enough players
                    min_players = self.get_min_players(session)
                    if min_players > 0 and len(session.players) < min_players:
                        msg = f"{self.game_name} room {session.room_id} does not have enough players to start."
                        break
                    await self.setup_game(session, ctx.channel)
                    return
                msg = f"You are not in {self.game_name} room {session.room_id}."
                break
        await ctx.channel.send(content=msg, delete_after=15.0)

    #Quit an existing room the player is in.
    async def quit(self, ctx, room_id):
        #In case of no room ID specified
        if room_id == None:
            msg = f"Please specify a room ID to quit as `!{self.game_abbrev} quit XXXX` or use `!{self.game_abbrev} quit all`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Quit all rooms a player is in.
        if room_id.lower() in ["all", "every", "everything"]:
            rooms_quit = 0
            for session in reversed(self.game_sessions):
                if any(ctx.author.id == player.user.id for player in session.players):
                    rooms_quit += 1
                    await self.remove_player(session, ctx.author)
            msg = f"{ctx.author.name} is not in any {self.game_name} rooms."
            if rooms_quit > 0:
                msg = f"Removed {ctx.author.name} from {rooms_quit} {self.game_name} room(s)."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Quit a specific room
        msg = f"{self.game_name} room {room_id} not found."
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                if any(ctx.author.id == player.user.id for player in session.players):
                    await self.remove_player(session, ctx.author)
                    msg = f"Removed {ctx.author.name} from {self.game_name} room {session.room_id}."
                    break
                msg = f"{ctx.author.name} is not in {self.game_name} room {session.room_id}."
                break
        await ctx.channel.send(content=msg, delete_after=15.0)
        return

    #Change the amount of players that can join a game.
    async def set_max_players(self, ctx, max_players, room_id):
        #With no arguments specified, send setting instructions.
        if max_players == None or room_id == None:
            msg = f"Please specify a maximum player count and a room ID to apply the setting to as `!{self.game_abbrev} set players YY XXXX`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return None
        #Check if an integer was supplied.
        if max_players.isdigit() == False or int(max_players) == 0:
            msg = "Please specify a positive integer for the maximum player count."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return None
        #Set max_players for supplied room_id.
        msg = f"{self.game_name} room {room_id} not found."
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                if any(ctx.author.id == player.user.id for player in session.players):
                    if self.has_game_started(session) == True:
                        msg = "Cannot change maximum player count after game has started."
                        break
                    msg = f"Maximum player count for {self.game_name} room {session.room_id} set to {max_players}."
                    await ctx.channel.send(content=msg, delete_after=15.0)
                    return int(max_players)
                msg = f"You are not in {self.game_name} room {session.room_id}."
                break
        await ctx.channel.send(content=msg, delete_after=15.0)
        return None

    #Change the amount of rounds a game will go on for.
    async def set_max_rounds(self, ctx, max_rounds, room_id):
        #With no arguments specified, send setting instructions.
        if max_rounds == None or room_id == None:
            msg = f"Please specify a total amount of rounds and a room ID to apply the setting to as `!{self.game_abbrev} set rounds YY XXXX`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return None
        #Check if an integer was supplied.
        if max_rounds.isdigit() == False or int(max_rounds) == 0:
            msg = "Please specify a positive integer for the total amount of rounds."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return None
        #Set max_rounds for supplied room_id.
        msg = f"{self.game_name} room {room_id} not found."
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                if any(ctx.author.id == player.user.id for player in session.players):
                    if self.has_game_started(session) == True:
                        msg = "Cannot change maximum amount of rounds after game has started."
                        break
                    msg = f"Total amount of rounds for {self.game_name} room {session.room_id} set to {max_rounds}."
                    await ctx.channel.send(content=msg, delete_after=15.0)
                    return int(max_rounds)
                msg = f"You are not in {self.game_name} room {session.room_id}."
                break
        await ctx.channel.send(content=msg, delete_after=15.0)
        return None
