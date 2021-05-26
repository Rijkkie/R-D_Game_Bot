import discord
from discord.ext import commands
from datetime import datetime
from database import dbfunctions
from database import dbembeds


class DatabaseEventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        # On startup, puts all the guilds and users who aren't bots in the database.
        for guild in self.client.guilds:
            dbfunctions.update_guild(guild)
        for user in self.client.users:
            if not user.bot:
                dbfunctions.update_user(user)
        print("DatabaseEvents cog loaded.")

    # Events, which keeps the user and guild data up to date.
    @commands.Cog.listener()
    async def on_member_join(self, user):
        dbfunctions.update_user(user)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        dbfunctions.update_user(after)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        dbfunctions.update_guild(guild)
        for user in self.client.users:
            if not user.bot:
                dbfunctions.update_user(user)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        dbfunctions.update_guild(guild, datetime.now())


    # Commands  # add aliases
    @commands.command(aliases=['bal', 'money'])
    async def balance(self, ctx, user: discord.Member = None):
        # If the discord converter cannot find the user from the command argument, shows the invokers stats instead.
        if not user:
            user = ctx.author
        # Prevents a lookup on bots to prevent them in the database and shows the invokers stats instead.
        if user.bot:
            await self.stats(ctx)
            return
        # Updates the user, retrieves the balance and rank and then sends an embed.
        dbfunctions.update_user(user)
        balance = dbfunctions.get_balance(user.id)
        rank = dbfunctions.balance_rank(user.id)
        await ctx.send(embed=dbembeds.balance(user, balance, rank))


    @commands.command()
    async def stats(self, ctx, user: discord.Member = None):
        # If the discord converter cannot find the user from the command argument, shows the invokers stats instead.
        if not user:
            user = ctx.author
        # Prevents a lookup on bots to prevent them in the database and shows the invokers stats instead.
        if user.bot:
            await self.stats(ctx)
            return
        # Updates the user in the database and retrieves the user's stats.
        dbfunctions.update_user(user)
        stats = dbfunctions.get_stats(user.id)
        # Retrieves all the user's ranks from all the games
        ranks = []
        for i in range(len(stats)):
            ranks.append(dbfunctions.stats_rank(stats[i][0], user.id))
        # Retrieves the sum of the stats and score rank and uses all the retrieved/calculated data to send an embed.
        total_stats = dbfunctions.total_boardgame_stats(user.id)
        total_rank = dbfunctions.total_boardgame_rank(user.id)
        await ctx.send(embed=dbembeds.stats(user, stats, ranks, total_stats, total_rank))


    # Add per server? Same with stats
    @commands.command(aliases=['topbal', 'topbalance'])
    async def top_balance(self, ctx, page=1):
        # Calculates the offset which is needed to search in pages in the database, where negative pages aren't allowed.
        offset = page * 10 - 10
        if offset < 0:
            await ctx.send("Try a valid page number!")
            return
        # Retrieves the top balance data from the page in the database. Checks for invalid pages.
        # Calculates the ranks respectively from each user where same ranks are possible and then an embed is sent.
        top = dbfunctions.top_balance(offset)
        if not top:
            await ctx.send("Try a valid page number!")
            return
        elif offset > 0:
            ranks = top_ranks(top, dbfunctions.balance_rank(top[0][3]))
        else:
            ranks = top_ranks(top, 1)
        await ctx.send(embed=dbembeds.top_balance(top, ranks, page))


    @commands.command(aliases=['topstats', 'topboardgame', 'topscore'])
    async def top_stats(self, ctx, page=1):
        # Calculates the offset which is needed to search in pages in the database, where negative pages aren't allowed.
        offset = page * 10 - 10
        if offset < 0:
            await ctx.send("Try a valid page number!")
            return
        # Retrieves the top stats data from the page in the database. Checks for invalid pages.
        top = dbfunctions.top_boardgame(offset)
        if not top:
            await ctx.send("Try a valid page number!")
            return
        # Calculates the ranks respectively from each user where same ranks are possible and then an embed is sent.
        elif offset > 0:
            ranks = top_ranks(top, dbfunctions.total_boardgame_rank(top[0][0]))
        else:
            ranks = top_ranks(top, 1)
        await ctx.send(embed=dbembeds.top_boardgame(top, ranks, page))


    # For the other games maybe, blackjack, hangman, etc. which sums up all the scores and not just boardgames.
    # @commands.command()
    # async def top_score(self, ctx):
    #     pass


    # Local error handling
    @balance.error
    async def events_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await self.balance(ctx)
            return
        raise error


def top_ranks(top, topmost_rank):
    # Gives the ranks respectively from each user's balance where same rank placing is possible.
    ranks = [topmost_rank]
    for i in range(1, len(top)):
        if top[i - 1][1] == top[i][1]:
            ranks.append(ranks[i - 1])
        else:
            ranks.append(ranks[i - 1] + 1)
    return ranks


def setup(client):
    client.add_cog(DatabaseEventsCog(client))
