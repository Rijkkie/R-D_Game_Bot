import mysql.connector as mysql
import json

with open("./config.json") as config_file:
    config = json.load(config_file)
cnx = mysql.connect(**config["mysql"])
cursor = cnx.cursor()

sqlFile = open('database/dbscripts/queries.sql', 'r')
sqlQueries = sqlFile.read().split(';')
sqlFile.close()


# The view 'balance' has a standard money value for every user (1000) that is implemented on the database,
# so it is a little bit more of a hassle to change that value.
# The same goes for the view 'stats' with 100 points per win, 50 per draw and 10 per loss.
# Also, not really sure if I should separate the queries from the functions and place them in queries.sql or not
# But it makes this file look a bit cleaner.


# Used for updating the user.
def update_user(user):
    values = {'user_id': user.id, 'name': user.name, 'discriminator': user.discriminator}
    execute_query(sqlQueries[0], values)


# Used for updating the guild.
def update_guild(guild, left_at=None):
    values = {'guild_id': guild.id, 'name': guild.name, 'icon': str(guild.icon_url), 'left_at': left_at}
    execute_query(sqlQueries[1], values)


# Used for increasing or decreasing the money for a specific user inserted into the database.
def transaction(user_id, guild_id, amount="100"):
    values = (user_id, guild_id, amount)
    execute_query(sqlQueries[2], values)


# Used for inserting the game outcomes into the database.
def boardgame_action(game, user_id, guild_id, wld):
    values = (game, user_id, guild_id, wld)
    execute_query(sqlQueries[3], values)


# Used to retrieve the balance of a specific user.
def get_balance(user_id):
    return retrieve_query(sqlQueries[4], (user_id,))[0][0]


# Used to retrieve the stats of a specific user.
def get_stats(user_id):
    return retrieve_query(sqlQueries[5], (user_id,))


# Used to retrieve the balance rank of a specific user.
def balance_rank(user_id):
    count = retrieve_query(sqlQueries[6], (user_id,))[0][0]
    return 1 if (count == 0) else count + 1


# Used to retrieve the stats rank of a specific user and specific game.
def stats_rank(game, user_id):
    values = {'game': game, 'user_id': user_id}
    count = retrieve_query(sqlQueries[7], values)[0][0]
    return 1 if (count == 0) else count + 1


# Used to retrieve the sum of the boardgame stats of a specific user.
def total_boardgame_stats(user_id):
    return retrieve_query(sqlQueries[8], (user_id,))


# Used to retrieve the global rank of the boardgames of a specified user
def total_boardgame_rank(user_id):
    count = retrieve_query(sqlQueries[9], (user_id,))[0][0]
    return 1 if (count == 0) else count + 1


# Used to retrieve a leaderboard page of the global balances in descending order.
def top_balance(offset):
    return retrieve_query(sqlQueries[10], (offset,))


# Used to retrieve a leaderboard page of the global stats in descending order.
def top_boardgame(offset):
    return retrieve_query(sqlQueries[11], (offset,))


def retrieve_query(query, values):
    cursor.execute(query, values)
    retrieved_data = cursor.fetchall()
    return retrieved_data


def execute_query(query, values):
    cursor.execute(query, values)
    cnx.commit()
