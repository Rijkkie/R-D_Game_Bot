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
        # Creates the database/tables if they did not exist already.
        # dbfunctions.db_startup()  # Had to remove this function, because the database sometimes kept hanging.
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
        await ctx.send(embed=dbembeds.balance(user, balance))


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
        # Gets the stats from every game of the specified user.
        games = dbfunctions.get_games()
        stats = []
        for i in range(len(games)):
            stats.append(dbfunctions.get_stats(games[i][0], user.id))
        # Retrieves the sum of the stats and score rank needed for the embed.
        total_stats = dbfunctions.total_boardgame_stats(user.id)
        # Checks if total_stats is not None, which might be because there are no games in the database yet.
        if not total_stats:
            await ctx.send("No boardgames have been played yet! Play a game first!")
            return
        await ctx.send(embed=dbembeds.stats(user, stats, total_stats))


    # Add per server? Same with stats
    @commands.command(aliases=['topbal', 'topbalance'])
    async def top_balance(self, ctx, page=1):
        # Calculates the offset which is needed to search in pages in the database, where negative pages aren't allowed.
        offset = page * 10 - 10
        if offset < 0:
            await ctx.send("Try a valid page number!")
            return
        # Retrieves the top balance data from the page in the database. Checks for invalid pages.
        top = dbfunctions.top_balance(offset)
        if not top:
            await ctx.send("Try a valid page number!")
            return
        await ctx.send(embed=dbembeds.top_balance(top, page))


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
            await ctx.send("An invalid page number has been given or no games have been played yet!")
            return
        await ctx.send(embed=dbembeds.top_boardgame(top, page))


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


def setup(client):
    client.add_cog(DatabaseEventsCog(client))
