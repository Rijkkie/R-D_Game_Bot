import discord
from discord.ext import commands
from datetime import datetime
from database import dbfunctions
from database import dbembeds


class DatabaseEventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            dbfunctions.update_guild(guild)
        for user in self.client.users:  # Will not filter bots since some users might check stats of bots for no reason.
            dbfunctions.update_user(user)
        print("DatabaseEvents cog loaded.")


    @commands.Cog.listener()
    async def on_member_join(self, user):
        dbfunctions.update_user(user)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        dbfunctions.update_user(after)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        dbfunctions.update_guild(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        dbfunctions.update_guild(guild, datetime.now())


    # Commands  # add aliases
    @commands.command(aliases=['bal', 'money'])  # Check balance of other people(arg), aliases(bal, etc.), top balances, per server(view)?
    async def balance(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        dbfunctions.update_user(user)
        balance = dbfunctions.get_balance(user.id)
        rank = dbfunctions.balance_rank(user.id)
        await ctx.send(embed=dbembeds.balance(user, balance, rank))

    @commands.command()  # NEED EMBED, users that arent in stats table! # remove game parameter
    async def stats(self, ctx, user: discord.Member = None):
        if not user:
            user = ctx.author
        dbfunctions.update_user(user)
        stats = dbfunctions.get_stats(user.id)
        ranks = []
        for i in range(len(stats)):
            ranks.append(dbfunctions.stats_rank(stats[i][0], user.id))
        total_stats = dbfunctions.total_boardgame_stats(user.id)
        total_rank = dbfunctions.total_boardgame_rank(user.id)
        await ctx.send(embed=dbembeds.stats(user, stats, ranks, total_stats, total_rank))

    @commands.command()
    async def topbalance(self, ctx):
        pass

    @commands.command()
    async def topboardgame(self, ctx):
        pass

    @commands.command()
    async def topscore(self, ctx):
        pass

    # @commands.command()  # NEED EMBED, score, per server?
    # async def leaderboard(self, ctx):
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
