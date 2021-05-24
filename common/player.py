#===============================================================================
# Session v1.0
# - Last Updated: 22 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 22 May 2021 - File started and finished. -YJ
#===============================================================================
# Notes
# ..............................................................................
#
#===============================================================================
# Description
# ..............................................................................
# player.py holds the basic, shared info and functions used for players of
# various games run by the bot.
#===============================================================================

#Import Modules
from discord import User

#Player Class
#A base class to extend in specific game's classes, if needed. Create as
#Player(user) where user is a discord user. After creation, user can be called.
class Player:
    #Define variables.
    def __init__(self, user: User):
        self.__user = user

    @property
    def user(self):
        return self.__user
