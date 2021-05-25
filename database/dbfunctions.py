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
# But it makes this file look way cleaner.


def update_user(user):
    values = {'user_id': user.id, 'name': user.name, 'discriminator': user.discriminator}
    execute_query(sqlQueries[0], values)


def update_guild(guild, left_at=None):
    values = {'guild_id': guild.id, 'name': guild.name, 'icon': str(guild.icon_url), 'left_at': left_at}
    execute_query(sqlQueries[1], values)


def transaction(user_id, guild_id, amount="100"):
    values = (user_id, guild_id, amount)
    execute_query(sqlQueries[2], values)


def boardgame_action(game, user_id, guild_id, wld):
    values = (game, user_id, guild_id, wld)
    execute_query(sqlQueries[3], values)


def get_balance(user_id):
    return retrieve_query(sqlQueries[4], (user_id,))[0][0]


def get_stats(user_id):
    return retrieve_query(sqlQueries[5], (user_id,))


def balance_rank(user_id):
    count = retrieve_query(sqlQueries[6], (user_id,))[0][0]
    return 1 if (count == 0) else count + 1


def stats_rank(game, user_id):
    values = {'game': game, 'user_id': user_id}
    count = retrieve_query(sqlQueries[7], values)[0][0]
    return 1 if (count == 0) else count + 1


def total_boardgame_stats(user_id):
    return retrieve_query(sqlQueries[8], (user_id,))


def total_boardgame_rank(user_id):
    count = retrieve_query(sqlQueries[9], (user_id,))[0][0]
    return 1 if (count == 0) else count + 1


def top_score():
    pass


def retrieve_query(query, values):
    cursor.execute(query, values)
    retrieved_data = cursor.fetchall()
    return retrieved_data


def execute_query(query, values):
    cursor.execute(query, values)
    cnx.commit()
