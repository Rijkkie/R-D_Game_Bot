#===============================================================================
# Common v1.3
# - Last Updated: 17 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 17 May 2021 - Added Card class and changed card_to_emoji to a dict. Also,
#               made card_deck_52 better. -YJ
# 30 Apr 2021 - Adjustments because sessions are Classes now; Now emoji/number
#               returns None; Added quit_room, card_deck_52, card_to_emoji. -YJ
# 24 Apr 2021 - added two extra functions maybe? -RK
# 18 Apr 2021 - Started and finished file; Added generate_room_id, join_room,
#               number_to_emoji, and emoji_to_number. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Split this file into several files that can be imported separately. -YJ
# - Add an expiry timer on that room ID or something, to prevent users from just
#   starting a bunch of empty rooms and hogging all the IDs. -YJ
# - A lot more room stuff could be made into common code. -YJ
#===============================================================================
# Description
# ..............................................................................
# common.py contains common features of the bot's games, such as registering
# game rooms, or creating and shuffling card decks.
#===============================================================================

#Import Modules
import random

#Card Dict
card_emoji = {
    "Hearts": {
        1: "<:HA:716858601041428502>",
        2: "<:H2:716858631936671804>",
        3: "<:H3:716858652752871485>",
        4: "<:H4:716858669446332426>",
        5: "<:H5:716858683857829890>",
        6: "<:H6:716858697732718684>",
        7: "<:H7:716858732557893632>",
        8: "<:H8:716858746474725386>",
        9: "<:H9:716858760450146384>",
        10: "<:H10:716858775570481223>",
        11: "<:HJ:716858817094090832>",
        12: "<:HQ:716858849868513341>",
        13: "<:HK:716858861247791196>"
    },
    "Diamonds": {
        1: "<:DA:716858907821342740>",
        2: "<:D2:716858925395476510>",
        3: "<:D3:716858934874341446>",
        4: "<:D4:716858950133350444>",
        5: "<:D5:716858961730732043>",
        6: "<:D6:716858984522580008>",
        7: "<:D7:716858996459307088>",
        8: "<:D8:716859011491954720>",
        9: "<:D9:716859023093399643>",
        10: "<:D10:716859063111254018>",
        11: "<:DJ:716859091942899784>",
        12: "<:DQ:716859115149852722>",
        13: "<:DK:716859126088728607>"
    },
    "Spades": {
        1: "<:SA:716859337850748979>",
        2: "<:S2:716859353390383176>",
        3: "<:S3:716859364945952788>",
        4: "<:S4:716859377793105980>",
        5: "<:S5:716859390275354624>",
        6: "<:S6:716859401415426080>",
        7: "<:S7:716859412697841776>",
        8: "<:S8:716859444427882556>",
        9: "<:S9:716859456889028679>",
        10: "<:S10:716859469392379975>",
        11: "<:SJ:716859500518440961>",
        12: "<:SQ:716859517417029652>",
        13: "<:SK:716859531400839178>"
    },
    "Clubs": {
        1: "<:CA:716859547956019250>",
        2: "<:C2:716859561998418021>",
        3: "<:C3:716859569946492959>",
        4: "<:C4:716859578154876929>",
        5: "<:C5:716859589160730674>",
        6: "<:C6:716859596479922297>",
        7: "<:C7:716859608131698751>",
        8: "<:C8:716859613676437514>",
        9: "<:C9:716859631120547922>",
        10: "<:C10:716859635826556980>",
        11: "<:CJ:716859641388335124>",
        12: "<:CQ:716859653182718083>",
        13: "<:CK:716859657972350977>"
    }
}

#Card Setup
class Card:
    #Define variables
    def __init__(self, suit: str, value: int):
        self.__suit = suit
        self.__value = value
        self.__emoji = card_emoji[suit][value]

    @property
    def suit(self):
        return self.__suit

    @property
    def value(self):
        return self.__value

    @property
    def emoji(self):
        return self.__emoji


#Common Functions
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
    deck = []
    for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
        for value in range(1, 14):
            card = Card(suit, value)
            deck.append(card)
    return deck

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
