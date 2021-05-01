#===============================================================================
# Common v1.2
# - Last Updated: 30 Apr 2021
#===============================================================================
# Update History
# ..............................................................................
# 30 Apr 2021 - Adjustments because sessions are Classes now; Now emoji/number
#               returns None; Added quit_room, card_deck_52, card_to_emoji. -YJ
# 24 Apr 2021 - added two extra functions maybe? -RK
# 18 Apr 2021 - Started and finished file; Added generate_room_id, join_room,
#               number_to_emoji, and emoji_to_number. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Split this file into several files that can be imported separately. -YJ
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
            if session.room_id == room_id:
                room_id = ""
                break
    return room_id

def join_room(game_sessions, room_id, player, max_players):
    #Check for existence of room ID
    for session in game_sessions:
        if session.room_id == room_id:
            for player_in_session in session.players:
                if player_in_session == player:
                    return 1 #Player is already in the room.
            if max_players > 0 and len(session.players) >= max_players:
                return 2 #Room is full.
            session.add_player(player)
            return 0 #Player was not in the room; Added player to room.
    return 3 #Room ID not found in any sessions.

def quit_room(game_sessions, room_id, player):
    #Check for existence of room ID
    for session in game_sessions:
        if session.room_id == room_id:
            for player_in_session in session.players:
                if player_in_session.id == player.id:
                    session.remove_player(player)
                    return 0 #Player was in the room; Removed player from room.
            return 1 #Player was not in the room.
    return 2 #Room ID not found in any sessions.

def card_deck_52():
    #Would it be less efficient to have a for-loop generate this? It'd look better, but...
    return ["1 h","2 h","3 h","4 h","5 h","6 h","7 h","8 h","9 h","10 h","11 h","12 h","13 h",
            "1 d","2 d","3 d","4 d","5 d","6 d","7 d","8 d","9 d","10 d","11 d","12 d","13 d",
            "1 s","2 s","3 s","4 s","5 s","6 s","7 s","8 s","9 s","10 s","11 s","12 s","13 s",
            "1 c","2 c","3 c","4 c","5 c","6 c","7 c","8 c","9 c","10 c","11 c","12 c","13 c"]

def card_to_emoji(card):
    if card == "1 h": #Hearts
        return "<:HA:716858601041428502>"
    if card == "2 h":
        return "<:H2:716858631936671804>"
    if card == "3 h":
        return "<:H3:716858652752871485>"
    if card == "4 h":
        return "<:H4:716858669446332426>"
    if card == "5 h":
        return "<:H5:716858683857829890>"
    if card == "6 h":
        return "<:H6:716858697732718684>"
    if card == "7 h":
        return "<:H7:716858732557893632>"
    if card == "8 h":
        return "<:H8:716858746474725386>"
    if card == "9 h":
        return "<:H9:716858760450146384>"
    if card == "10 h":
        return "<:H10:716858775570481223>"
    if card == "11 h":
        return "<:HJ:716858817094090832>"
    if card == "12 h":
        return "<:HQ:716858849868513341>"
    if card == "13 h":
        return "<:HK:716858861247791196>"
    if card == "1 d": #Diamonds
        return "<:DA:716858907821342740>"
    if card == "2 d":
        return "<:D2:716858925395476510>"
    if card == "3 d":
        return "<:D3:716858934874341446>"
    if card == "4 d":
        return "<:D4:716858950133350444>"
    if card == "5 d":
        return "<:D5:716858961730732043>"
    if card == "6 d":
        return "<:D6:716858984522580008>"
    if card == "7 d":
        return "<:D7:716858996459307088>"
    if card == "8 d":
        return "<:D8:716859011491954720>"
    if card == "9 d":
        return "<:D9:716859023093399643>"
    if card == "10 d":
        return "<:D10:716859063111254018>"
    if card == "11 d":
        return "<:DJ:716859091942899784>"
    if card == "12 d":
        return "<:DQ:716859115149852722>"
    if card == "13 d":
        return "<:DK:716859126088728607>"
    if card == "1 s": #Spades
        return "<:SA:716859337850748979>"
    if card == "2 s":
        return "<:S2:716859353390383176>"
    if card == "3 s":
        return "<:S3:716859364945952788>"
    if card == "4 s":
        return "<:S4:716859377793105980>"
    if card == "5 s":
        return "<:S5:716859390275354624>"
    if card == "6 s":
        return "<:S6:716859401415426080>"
    if card == "7 s":
        return "<:S7:716859412697841776>"
    if card == "8 s":
        return "<:S8:716859444427882556>"
    if card == "9 s":
        return "<:S9:716859456889028679>"
    if card == "10 s":
        return "<:S10:716859469392379975>"
    if card == "11 s":
        return "<:SJ:716859500518440961>"
    if card == "12 s":
        return "<:SQ:716859517417029652>"
    if card == "13 s":
        return "<:SK:716859531400839178>"
    if card == "1 c": #Clubs
        return "<:CA:716859547956019250>"
    if card == "2 c":
        return "<:C2:716859561998418021>"
    if card == "3 c":
        return "<:C3:716859569946492959>"
    if card == "4 c":
        return "<:C4:716859578154876929>"
    if card == "5 c":
        return "<:C5:716859589160730674>"
    if card == "6 c":
        return "<:C6:716859596479922297>"
    if card == "7 c":
        return "<:C7:716859608131698751>"
    if card == "8 c":
        return "<:C8:716859613676437514>"
    if card == "9 c":
        return "<:C9:716859631120547922>"
    if card == "10 c":
        return "<:C10:716859635826556980>"
    if card == "11 c":
        return "<:CJ:716859641388335124>"
    if card == "12 c":
        return "<:CQ:716859653182718083>"
    if card == "13 c":
        return "<:CK:716859657972350977>"
    return None

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
    return None

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
    return None
   
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
