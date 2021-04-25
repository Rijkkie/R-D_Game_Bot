#===============================================================================
# Common v1.0
# - Last Updated: 24 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 24 Apr 2021 - added two extra functions maybe?
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
   
def string_to_emoji(word):
    emojis = ""
    letters = word.upper()
    for i in letters:
        if ord(i) in range(65,91):
            if i == "A":
                emojis += ":regional_indicator_a:"
            if i == "B":
                emojis += ":regional_indicator_b:"
            if i == "C":
                emojis += ":regional_indicator_c:"
            if i == "D":
                emojis += ":regional_indicator_d:"
            if i == "E":
                emojis += ":regional_indicator_e:"
            if i == "F":
                emojis += ":regional_indicator_f:"
            if i == "G":
                emojis += ":regional_indicator_g:"
            if i == "H":
                emojis += ":regional_indicator_h:"
            if i == "I":
                emojis += ":regional_indicator_i:"
            if i == "J":
                emojis += ":regional_indicator_j:"
            if i == "K":
                emojis += ":regional_indicator_k:"
            if i == "L":
                emojis += ":regional_indicator_l:"
            if i == "M":
                emojis += ":regional_indicator_m:"
            if i == "N":
                emojis += ":regional_indicator_n:"
            if i == "O":
                emojis += ":regional_indicator_o:"
            if i == "P":
                emojis += ":regional_indicator_p:"
            if i == "Q":
                emojis += ":regional_indicator_q:"
            if i == "R":
                emojis += ":regional_indicator_r:"
            if i == "S":
                emojis += ":regional_indicator_s:"
            if i == "T":
                emojis += ":regional_indicator_t:"
            if i == "U":
                emojis += ":regional_indicator_u:"
            if i == "V":
                emojis += ":regional_indicator_v:"
            if i == "W":
                emojis += ":regional_indicator_w:"
            if i == "X":
                emojis += ":regional_indicator_x:"
            if i == "Y":
                emojis += ":regional_indicator_y:"
            if i == "Z":
                emojis += ":regional_indicator_z:"
        elif ord(i) in range(48,58):
            emojis += number_to_emoji(int(i))
        else:
            emojis += ":asterisk:"
    return emojis

def create_winner_message(winner):
    winner_message = ":clap::regional_indicator_h::regional_indicator_a::regional_indicator_s::regional_indicator_w::regional_indicator_o::regional_indicator_n::regional_indicator_t::regional_indicator_h::regional_indicator_e::regional_indicator_g::regional_indicator_a::regional_indicator_m::regional_indicator_e::clap:"
    audience = ":clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap::clap:"
    message_length = 15
    clap = ":clap:"
    if len(winner)>message_length:
            return audience + "\n" + winner_message + "\n" + audience
    else:
        start_position = 7
        start_position = start_position - int(len(winner)/2)
        end = 15 - start_position - len(winner)
        winner_name = ""
        for i in range(start_position):
            winner_name += clap
        winner_name += string_to_emoji(winner)
        for i in range(end):
            winner_name += clap
        return audience +"\n" +  winner_name + "\n"  + winner_message + "\n" + audience

