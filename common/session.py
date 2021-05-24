#===============================================================================
# Session v1.0
# - Last Updated: 22 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 22 May 2021 - =Split generate_room_id from common.py; Added Session class.
#               -YJ
# 18 Apr 2021 - Started and finished common.py; Added generate_room_id. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Add an expiry timer on that room ID or something, to prevent users from just
#   starting a bunch of empty rooms and hogging all the IDs. -YJ
# - A lot more room stuff could be made into common code. -YJ
#===============================================================================
# Description
# ..............................................................................
# session.py holds the basic, shared info and functions used for sessions of
# various games run by the bot.
#===============================================================================

#Import Modules
from discord import Message, User
from common.player import Player
import random

#Generate Room ID
#Generate a new unique ID for game room
def generate_room_id(game_sessions):
    room_id = ""
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
                "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    while room_id == "":
        for _ in range(4):
            room_id += random.choice(alphabet)
        for session in game_sessions:
            if session.room_id == room_id:
                room_id = ""
                break
    return room_id

#Session Class
#A base class to extend in specific game's classes, if needed. Create as
#Session(game_sessions) where game_sessions is an array of other sessions.
#The class generates a room_id upon creation.
class Session:
    #Define variables.
    def __init__(self, game_sessions):
        self.__room_id = generate_room_id(game_sessions)
        self.__players = []
        self.__message_join = None

    @property
    def room_id(self):
        return self.__room_id

    @property
    def players(self):
        return self.__players

    @property
    def message_join(self):
        return self.__message_join

    @message_join.setter
    def message_join(self, message_join: Message):
        self.__message_join = message_join

    #Add players.
    def add_player(self, player: Player):
        if not any(player.user.id == active_player.user.id for active_player in self.__players):
            self.__players.append(player)

    #Remove player.
    def remove_player(self, user: User):
        for player in reversed(self.__players):
            if player.user.id == user.id:
                self.__players.remove(player)

    #Shuffle players.
    def shuffle_players(self):
        random.shuffle(self.__players)
