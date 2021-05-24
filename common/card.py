#===============================================================================
# Card v1.0
# - Last Updated: 23 May 2021
#===============================================================================
# Update History
# ..............................................................................
# 24 May 2021 - Moved card_emoji to emoji.py. -YJ
# 23 May 2021 - Split random_card from blackjack.py. -YJ
# 22 May 2021 - Split Card class, card_emoji, card_deck_52 from common.py. -YJ
# 17 May 2021 - Added Card class and changed card_emoji to a dict. Also,
#               made card_deck_52 better. -YJ
# 30 Apr 2021 - Started and finished common.py; Added card_deck_52, card_emoji.
#               -YJ
#===============================================================================
# Notes
# ..............................................................................
#
#===============================================================================
# Description
# ..............................................................................
# card.py holds the class and functions used for most common, shared features
# used for the bot's card games.
#===============================================================================

#Import Modules
from common.emoji import card_emoji

import random

#Standard Deck Elements
suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
values = range(1, 14)

#Card Class
#Create as Card(suit, value) where suit is a string and value is an integer from
#1 through 13, as seen in the dict card_emoji. After creation, suit and value
#can be called, as well as emoji which gets the discord emoji of the card.
class Card:
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

#Return an ordered standard 52-card deck as array.
def card_deck_52():
    deck = []
    for suit in suits:
        for value in values:
            card = Card(suit, value)
            deck.append(card)
    return deck

#Return a random card.
def random_card():
    suit = random.choice(suits)
    value = random.choice(values)
    card = Card(suit, value)
    return card
