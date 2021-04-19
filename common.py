#===============================================================================
# Common v1.0
# - Last Updated: 18 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 18 Apr 2021 - Started and finished file; Added generate_room_id, join_room,
#               number_to_emoji, and emoji_to_number.
#===============================================================================
# Notes
# ..............................................................................
# - Add more common features, like card deck stuff. -YJ
#===============================================================================
# Description
# ..............................................................................
# common.py contains common features of the bot's games, such as registering
# game rooms, or creating and shuffling card decks.
#===============================================================================

#Import Modules
import random

def generate_room_id(game_sessions):
    #Generate a new unique ID for game room
    room_id = ""
    while room_id == "":
        alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
                    "N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        for c in range(4):
            room_id += random.choice(alphabet)
        for session in game_sessions:
            if session[0] == room_id:
                room_id = ""
                break
    return room_id

def join_room(game_sessions, room_id, player_id, max_players):
    #Check for existence of room ID
    for session in game_sessions:
        if session[0] == room_id:
            for player in session[2]:
                if player == player_id:
                    #Player is already in the room.
                    return 1
            if max_players <= 0 and len(session[2]) >= max_players:
                #Room is full.
                return 2
            #Player is not in the room; Add player to room.
            session[2].append(player_id)
            return 0
    #Room ID not found in any sessions.
    return 3

def number_to_emoji(number):
    if number == 0:
        return "0️⃣"
    if number == 1:
        return "1️⃣"
    if number == 2:
        return "2️⃣"
    if number == 3:
        return "3️⃣"
    if number == 4:
        return "4️⃣"
    if number == 5:
        return "5️⃣"
    if number == 6:
        return "6️⃣"
    if number == 7:
        return "7️⃣"
    if number == 8:
        return "8️⃣"
    if number == 9:
        return "9️⃣"
    if number == 10:
        return "🔟"

def emoji_to_number(emoji):
    if emoji == "0️⃣":
        return 0
    if emoji == "1️⃣":
        return 1
    if emoji == "2️⃣":
        return 2
    if emoji == "3️⃣":
        return 3
    if emoji == "4️⃣":
        return 4
    if emoji == "5️⃣":
        return 5
    if emoji == "6️⃣":
        return 6
    if emoji == "7️⃣":
        return 7
    if emoji == "8️⃣":
        return 8
    if emoji == "9️⃣":
        return 9
    if emoji == "🔟":
        return 10
