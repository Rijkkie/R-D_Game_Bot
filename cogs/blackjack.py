#===============================================================================
# Blackjack v1.2
# - Last Updated: 02 Jun 2021
#===============================================================================
# Update History
# ..............................................................................
# 02 Jun 2021 - Added support for inactivity timer of sessions. -YJ
# 30 May 2021 - Reaction join now goes through cog's join() instead of Game's
#               join(), which allows for better specialization. -YJ
# 23 May 2021 - All classes now extend a base class. -YJ
# 19 May 2021 - Finished file. -YJ
# 12 May 2021 - Started file. -YJ
#===============================================================================
# Notes
# ..............................................................................
# - Add database support. -YJ
#===============================================================================
# Description
# ..............................................................................
# - Basic Outline
# blackjack.py is a game where between one and seven players play against the
# dealer (the bot). The goal of the game is to collect cards with a value that
# exceeds the value of the dealer's hand, without going over 21. Face cards are
# worth 10, and aces are worth either 11 or 1.
#
# - During the Round
# At the start of the round, before any cards are dealt, players place bets
# (between 1 and 100). Then, each player is dealt two cards face-up. If their
# two cards total 21, they have received a blackjack. The dealer also draws two
# cards, one of which is face-up and one is face-down. Players then repeatedly
# take turns choosing to be dealt another random card, or keep the hand they
# have. Players with a hand worth more than 21 are automatically eliminated from
# the round. As a risk-reward option, players may double down, which involves
# doubling their initial bet and being dealt one final card.
#
# - End of Round
# After all players have taken their turns, the dealer reveals their face-down
# card, and may draw cards until their hand exceeds 16. The dealer also loses if
# they exceed 21. Any players with a hand worth more than that of the dealer win
# the round and are returned their bet in double. Players that received a
# blackjack are returned their bet 2.5 times. Players with a hand worth as much
# as that of the dealer tie and are returned their bet once. Any players that
# have a worse hand than the dealer or exceeded 21 lose their bet.
#===============================================================================

#Import Modules
import discord
from discord import Message, User
from discord.ext import commands

from common.session import Session
from common.player import Player
from common.game import Game
from common.card import Card, random_card
from database import dbfunctions

import random
import math

#Player Class
class BlackjackPlayer(Player):
    def __init__(self, user: User, guild_id=None):
        Player.__init__(self, user)
        self.__hand = []
        self.__funds = 100
        self.__bet = 10
        self.__doubled_down = False
        self.__turn_finished = False
        self.__guild_id = guild_id

    @property
    def hand(self):
        return self.__hand

    @property
    def funds(self):
        return self.__funds

    @property
    def bet(self):
        return self.__bet

    @property
    def doubled_down(self):
        return self.__doubled_down

    @property
    def turn_finished(self):
        return self.__turn_finished

    @property
    def guild_id(self):
        return self.__guild_id

    @property
    def value(self):
        value = 0
        has_ace = False
        for card in self.__hand:
            value += min(10, card.value)
            if card.value == 1:
                has_ace = True
        if has_ace and value+10 <= 21:
            value += 10
        return value

    @doubled_down.setter
    def doubled_down(self, truth: bool):
        self.__doubled_down = truth

    @turn_finished.setter
    def turn_finished(self, truth: bool):
        self.__turn_finished = truth

    @hand.setter
    def hand(self, hand):
        self.__hand = hand

    @bet.setter
    def bet(self, amount: int):
        self.__bet = amount

    @funds.setter
    def funds(self, amount: int):
        self.__funds = amount

    #Add a card.
    def give_card(self, card: Card):
        self.__hand.append(card)

#Session Class
class BlackjackSession(Session):
    def __init__(self, parent):
        Session.__init__(self, parent)
        self.__max_players = 7
        self.__dealer = BlackjackPlayer(None)
        self.__betting_active = False
        self.__round = 0
        self.__max_rounds = 10
        self.__message_board = None

    @property
    def max_players(self):
        return self.__max_players

    @property
    def dealer(self):
        return self.__dealer

    @property
    def betting_active(self):
        return self.__betting_active

    @property
    def round(self):
        return self.__round

    @property
    def max_rounds(self):
        return self.__max_rounds

    @property
    def message_board(self):
        return self.__message_board

    @betting_active.setter
    def betting_active(self, truth: bool):
        self.__betting_active = truth

    @round.setter
    def round(self, round: int):
        self.__round = round

    @max_players.setter
    def max_players(self, max_players: int):
        self.__max_players = max_players

    @max_rounds.setter
    def max_rounds(self, max_rounds: int):
        self.__max_rounds = max_rounds

    @message_board.setter
    def message_board(self, message_board: Message):
        self.__message_board = message_board

#Cog Class
class BlackjackCog(Game):
    def __init__(self, client):
        Game.__init__(self, client)
        self.game_name = "Blackjack"
        self.game_abbrev = "bj"
        self.bet_min = 1
        self.bet_max = 100

    #Report successful load.
    @commands.Cog.listener()
    async def on_ready(self):
        print("Blackjack cog loaded.")

    #Secondary Functions
    #Game instructions
    def instructions(self):
        msg = "**Blackjack Help**\n"
        msg += "Collect cards in your hand that exceed the value of the dealer's hand, but don't go over 21! Face cards are worth 10, and aces are worth either 11 or 1. Hit to receive a card, stand to confirm you are done hitting. Double down to double your bet and receive one final card.\n"
        msg += "`!bj new`: Start a new room.\n"
        msg += "`!bj set`: Get details on how to edit the game settings of a room.\n"
        msg += "`!bj join XXXX`: Join an existing room with its room ID specified in place of XXXX.\n"
        msg += "`!bj start XXXX`: Start the game of a room you're in with its room ID specified in place of XXXX.\n"
        msg += "`!bj players XXXX`: Get a list of players in an existing room with its room ID specified in place of XXXX.\n"
        msg += "`!bj bet YY XXXX`: Bet in a room you're in with the bet amount specified in place of YY and the room ID in place of XXXX.\n"
        msg += "`!bj quit XXXX`: Quit a room you're in with its room ID specified in place of XXXX. The game continues if other players remain.\n"
        msg += "`!bj quit all`: Quit all rooms you're in. The games continue if other players remain."
        return msg

    #Get maximum amount of players of a session.
    def get_max_players(self, session):
        return session.max_players

    #Check whether a game has started yet.
    def has_game_started(self, session):
        return session.round > 0

    #Remove session on inactivity timeout.
    async def timeout_session(self, session):
        if session.message_board != None:
            msg = f"{self.game_name} room {session.room_id} has timed out due to inactivity."
            await session.message_board.edit(content=msg)
            await session.message_board.clear_reactions()
        await Game.timeout_session(self, session)

    #Generate game board message.
    def generate_board_message(self, session):
        msg = f"**Blackjack Room {session.room_id}"
        if session.round <= session.max_rounds:
            msg += f" - ROUND {session.round}/{session.max_rounds}**\n"
            if session.betting_active == True:
                msg += "Place your bets!\n"
                msg += f"Bet by typing `!bj bet YY {session.room_id}`, replacing YY with the amount.\n"
                msg += "⏹ - Confirm bet.\n\n"
            elif len(session.dealer.hand) == 1:
                msg += "Hit or stand?\n"
                msg += "🔼 - Hit.\n"
                msg += "⏹ - Stand.\n"
                msg += "⏬ - Double down.\n\n"
            else:
                msg += "Results!\n"
                msg += "⏹ - Continue.\n\n"
            if session.betting_active == False:
                msg += "Dealer: "
                for card in session.dealer.hand:
                    msg += f"{card.emoji}"
                if len(session.dealer.hand) == 1:
                    msg += "⬜"
                msg += f" ({session.dealer.value})\n\n"
        else:
            msg += " - GAME OVER**\n"
        for player in session.players:
            if session.round <= session.max_rounds:
                if player.turn_finished:
                    msg += "✅"
                else:
                    msg += "🟥"
            else:
                if player.funds == max(p.funds for p in session.players):
                    msg += "👑"
                else:
                    msg += "🔹"
                dbfunctions.transaction(player.user.id, player.guild_id, str(player.funds))
            msg += f" **${player.funds}** {player.user.mention}"
            if session.round <= session.max_rounds:
                msg += ": "
                for card in player.hand:
                    msg += f"{card.emoji}"
                if session.betting_active == False:
                    if player.value == 21 and len(player.hand) == 2:
                        msg += f" (BLACKJACK!)"
                    else:
                        msg += f" ({player.value})"
                if len(session.dealer.hand) <= 1:
                    msg += f" [BET {player.bet}]"
                else:
                    if player.value > 21 or (player.value < session.dealer.value and session.dealer.value <= 21):
                        msg += f" [LOSE -{player.bet}]"
                    elif player.value > session.dealer.value or session.dealer.value > 21:
                        if player.value == 21 and len(player.hand) == 2:
                            msg += f" [WIN +{math.floor(player.bet*1.5)}]"
                        else:
                            msg += f" [WIN +{player.bet}]"
                    else:
                        msg += " [DRAW +0]"
            msg += "\n"
        return msg

    #Change player bet to specified amount.
    async def adjust_bet(self, session, player, amount):
        player.bet = min(max(self.bet_min, amount), self.bet_max)
        msg = self.generate_board_message(session)
        await session.message_board.edit(content=msg)

    #Send betting message, add reactions.
    async def setup_beginround(self, session, channel):
        session.inactivity_timer_restart()
        session.betting_active = True
        session.dealer.hand = []
        for player in session.players:
            player.turn_finished = False
            player.hand = []
        msg = self.generate_board_message(session)
        session.message_board = await channel.send(msg)
        await session.message_board.add_reaction("⏹")

    #Deal cards, send hit/stand message, add reactions.
    async def setup_midround(self, session):
        session.inactivity_timer_restart()
        session.betting_active = False
        session.dealer.give_card(random_card())
        for player in session.players:
            player.turn_finished = False
            for _ in range(2):
                player.give_card(random_card())
        msg = self.generate_board_message(session)
        #session.message_board = await session.message_board.channel.send(msg)
        await session.message_board.edit(content=msg)
        await session.message_board.clear_reactions()
        await session.message_board.add_reaction("🔼")
        await session.message_board.add_reaction("⏹")
        await session.message_board.add_reaction("⏬")

    #Dealer draws until 17+, process wins/ties/losses.
    async def setup_endround(self, session):
        session.inactivity_timer_restart()
        while session.dealer.value < 17:
            session.dealer.give_card(random_card())
        for player in session.players:
            player.turn_finished = False
            if player.value > 21 or (player.value < session.dealer.value and session.dealer.value <= 21):
                player.funds -= player.bet
            elif player.value > session.dealer.value or session.dealer.value > 21:
                player.funds += player.bet
                if player.value == 21 and len(player.hand) == 2:
                    player.funds += math.floor(player.bet/2)
        msg = self.generate_board_message(session)
        await session.message_board.edit(content=msg)
        await session.message_board.clear_reactions()
        await session.message_board.add_reaction("⏹")

    #Go to next round, or end game after final round.
    async def reset_round(self, session):
        session.round += 1
        await session.message_board.edit(delete_after=4.0)
        if session.round <= session.max_rounds:
            for player in session.players:
                if player.doubled_down == True:
                    player.bet = math.floor(player.bet/2)
                    player.doubled_down = False
            await self.setup_beginround(session, session.message_board.channel)
            return
        msg = self.generate_board_message(session)
        await session.message_board.channel.send(msg)
        self.game_sessions.remove(session)

    #Setup the initial variables and message(s) of the game.
    async def setup_game(self, session, channel):
        await Game.setup_game(self, session, channel)
        session.round = 1
        await self.setup_beginround(session, channel)

    #Handle additional checks required when a player joins the game.
    async def add_player(self, session, user):
        await Game.add_player(self, session, user)
        if session.message_board != None:
            msg = self.generate_board_message(session)
            await session.message_board.edit(content=msg)

    #Handle additional checks required when a player quits the game.
    async def remove_player(self, session, user):
        session.remove_player(user)
        if session.message_board != None:
            if len(session.players) <= 0:
                await session.message_board.delete()
                self.game_sessions.remove(session)
                return
            msg = self.generate_board_message(session)
            await session.message_board.edit(content=msg)
            return
        if len(session.players) <= 0:
            self.game_sessions.remove(session)

    #Primary Functions
    #With no arguments specified, send game instructions.
    @commands.group(name="blackjack", aliases=["bj", "21"], invoke_without_command=True)
    async def blackjack(self, ctx):
        await ctx.channel.send(self.instructions())

    #Help command to receive instructions.
    @blackjack.command(aliases=["?", "info", "information", "instructions"])
    async def help(self, ctx):
        await ctx.channel.send(self.instructions())

    #See the list of players of a room.
    @blackjack.command(aliases=["player", "players", "playerlist", "playerslist", "players_list", "list"])
    async def player_list(self, ctx, room_id=None):
        await Game.player_list(self, ctx, room_id)

    #Register a new game room.
    @blackjack.command(aliases=["create", "register", "host"])
    async def new(self, ctx):
        session = BlackjackSession(self)
        player = BlackjackPlayer(ctx.author, ctx.guild.id)
        await Game.new(self, ctx, session, player)

    #Join an existing game room by message.
    @blackjack.command(aliases=["enter"])
    async def join(self, ctx, room_id=None):
        player = BlackjackPlayer(ctx.author, ctx.guild.id)
        await Game.join(self, ctx, room_id, player)

    #Start a game.
    @blackjack.command(aliases=["begin"])
    async def start(self, ctx, room_id=None):
        await Game.start(self, ctx, room_id)

    #Quit a room.
    @blackjack.command(aliases=["stop", "exit", "end", "leave"])
    async def quit(self, ctx, room_id=None):
        await Game.quit(self, ctx, room_id)

    #Bet by message.
    @blackjack.command(aliases=[])
    async def bet(self, ctx, bet=None, room_id=None):
        #With no arguments specified, send setting instructions.
        if bet == None or room_id == None:
            msg = "Please specify a bet amount and a room ID to bet in as `!bj bet YY XXXX`"
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Check if an integer was supplied.
        if bet.isdigit() == False:
            msg = "Please specify a number for the bet amount."
            await ctx.channel.send(content=msg, delete_after=15.0)
            return
        #Set a bet amount in the specified room ID.
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                for player in session.players:
                    if ctx.author.id == player.user.id:
                        if session.round > 0:
                            await self.adjust_bet(session, player, int(bet))
                            await ctx.message.delete()
                            return
                        msg = f"You cannot bet in a room where the game has not started."
                        await ctx.channel.send(content=msg, delete_after=15.0)
                        return
                msg = f"You are not in Blackjack room {session.room_id}."
                await ctx.channel.send(content=msg, delete_after=15.0)
                return
        msg = f"Blackjack room {room_id} not found."
        await ctx.channel.send(content=msg, delete_after=15.0)

    #Edit a room's settings.
    @blackjack.group(name="setting", aliases=["set", "settings", "edit", "mod", "modify", "rule", "rules"], invoke_without_command=True)
    async def setting(self, ctx, room_id=None):
        #With no arguments specified, send setting instructions.
        if room_id == None:
            msg = "**Blackjack Settings**\n"
            msg += "Several settings can be edited to suit the desired play experience. In each setting below, YY is to be replaced with a number, and XXXX with the room ID of the room you are changing settings for.\n"
            msg += "`!bj set XXXX`: See the current settings for a room.\n"
            msg += "`!bj set players YY XXXX`: The maximum amount of players that can join. Default is 7.\n"
            msg += "`!bj set rounds YY XXXX`: The amount of rounds to be played. Default is 10."
            await ctx.channel.send(msg)
            return
        #With only a room ID specified, show current settings for the room.
        for session in self.game_sessions:
            if room_id.upper() == session.room_id:
                msg = f"**Blackjack Room {session.room_id} Settings**\n"
                msg += f"Maximum Players: {session.max_players}\n"
                msg += f"Rounds: {session.max_rounds}"
                await ctx.channel.send(msg)
                return
        msg = f"Blackjack setting or room {room_id} not found."
        await ctx.channel.send(content=msg, delete_after=15.0)

    #Change the amount of players that can join a game.
    @setting.command(aliases=["player", "players", "maxplayer", "maxplayers", "max_player", "max_players", "playercount", "player_count", "totalplayers", "total_players"])
    async def set_max_players(self, ctx, max_players=None, room_id=None):
        return_value = await Game.set_max_players(self, ctx, max_players, room_id)
        if return_value != None:
            for session in self.game_sessions:
                if room_id.upper() == session.room_id:
                    session.max_players = return_value

    #Change the amount of rounds a game will go on for.
    @setting.command(aliases=["round", "rounds", "maxround", "maxrounds", "max_round", "max_rounds", "roundcount", "round_count", "totalrounds", "total_rounds"])
    async def set_max_rounds(self, ctx, max_rounds=None, room_id=None):
        #With no arguments specified, send setting instructions.
        return_value = await Game.set_max_rounds(self, ctx, max_rounds, room_id)
        if return_value != None:
            for session in self.game_sessions:
                if room_id.upper() == session.room_id:
                    session.max_rounds = return_value

    #Reaction handling
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        #Prevent bot's own reactions triggering this
        if user == self.client.user:
            return
        for session in self.game_sessions:
            #Joining game by reacting with play emoji
            if session.message_join != None and reaction.message.id == session.message_join.id and reaction.emoji == "▶️":
                ctx = await self.client.get_context(reaction.message)
                ctx.author = user
                await self.join(ctx, session.room_id)
                return

            #Taking turn by reacting with emoji
            if session.message_board != None and reaction.message.id == session.message_board.id:
                for player in session.players:
                    if player.user.id == user.id and player.turn_finished == False:
                        if session.betting_active:
                            if reaction.emoji == "⏹":
                                player.turn_finished = True
                                msg = self.generate_board_message(session)
                                await session.message_board.edit(content=msg)
                                if all(p.turn_finished == True for p in session.players):
                                    await self.setup_midround(session)
                                    return
                                await reaction.message.remove_reaction(reaction.emoji, user)
                            return
                        elif len(session.dealer.hand) == 1:
                            if reaction.emoji == "🔼":
                                player.give_card(random_card())
                                if player.value > 21:
                                    player.turn_finished = True
                            elif reaction.emoji == "⏹":
                                player.turn_finished = True
                            elif reaction.emoji == "⏬":
                                player.bet *= 2
                                player.give_card(random_card())
                                player.doubled_down = True
                                player.turn_finished = True
                            msg = self.generate_board_message(session)
                            await session.message_board.edit(content=msg)
                            if all(p.turn_finished == True for p in session.players):
                                await self.setup_endround(session)
                                return
                            await reaction.message.remove_reaction(reaction.emoji, user)
                            return
                        else:
                            if reaction.emoji == "⏹":
                                player.turn_finished = True
                                msg = self.generate_board_message(session)
                                await session.message_board.edit(content=msg)
                                if all(p.turn_finished == True for p in session.players):
                                    await self.reset_round(session)
                                    return
                                await reaction.message.remove_reaction(reaction.emoji, user)
                            return

#Client Setup
def setup(client):
    client.add_cog(BlackjackCog(client))
