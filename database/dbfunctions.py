import mysql.connector as mysql
import json
import os

path = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))
with open(str(path) + "/config.json", 'r') as config_file:
    config = json.load(config_file)
    config_file.close()
cnx = mysql.connect(**config["mysql"])
cursor = cnx.cursor()


# Whenever this function is called, it will create the database and tables if they did not already exist.
# def db_startup():
#     sql_file = open(str(path) + "/database/dbscripts/dbtables.sql", 'r')
#     sql_queries = sql_file.read().split(';')
#     for query in sql_queries:
#         cursor.execute(query)
#     cnx.commit()
#     sql_file.close()


# Used for updating the user.
def update_user(user):
    values = {'user_id': user.id, 'name': user.name, 'discriminator': user.discriminator}
    execute_query(sqlQueries["update_user"], values)


# Used for updating the guild.
def update_guild(guild, left_at=None):
    values = {'guild_id': guild.id, 'name': guild.name, 'icon': str(guild.icon_url), 'left_at': left_at}
    execute_query(sqlQueries["update_guild"], values)


# Used for increasing or decreasing the money for a specific user inserted into the database.
def transaction(user_id, guild_id, amount="100"):
    values = (user_id, guild_id, amount)
    execute_query(sqlQueries["transaction"], values)


# Used for inserting the game outcomes into the database.
def boardgame_action(game, user_id, guild_id, wld):
    values = (game, user_id, guild_id, wld)
    execute_query(sqlQueries["boardgame_action"], values)


# Used to retrieve the balance of a specific user.
def get_balance(user_id):
    return retrieve_query(sqlQueries["get_balance"], (user_id,))[0]


# Used to retrieve the stats of a specific user.
def get_stats(game, user_id):
    return retrieve_query(sqlQueries["get_stats"], (game, user_id))


# Used to get all the games in the database.
def get_games():
    return retrieve_query(sqlQueries["get_games"], None)


# Used to get the user from the database with the given userid.
def get_user(user_id):
    return retrieve_query(sqlQueries["get_user"], (user_id,))


# Used to retrieve the sum of the boardgame stats and their rank of a specific user.
def total_boardgame_stats(user_id):
    return retrieve_query(sqlQueries["total_boardgame_stats"], (user_id,))


# Used to retrieve a leaderboard page of the global balances in descending order.
def top_balance(offset):
    return retrieve_query(sqlQueries["top_balance"], (offset,))


# Used to retrieve a leaderboard page of the global stats in descending order.
def top_boardgame(offset):
    return retrieve_query(sqlQueries["top_boardgame"], (offset,))


def app_topbal():
    return retrieve_query(sqlQueries["app_topbal"], None)


def app_topboardgame():
    return retrieve_query(sqlQueries["app_topboardgame"], None)


def search_names(name):
    wildcards = '%' + name.lower() + '%'
    return retrieve_query(sqlQueries["search_names"], (wildcards,))


# Returns the columns of the results of the given query from the database.
def retrieve_query(query, values):
    if not cnx.is_connected():
        cnx.reconnect()
    cursor.execute(query, values)
    retrieved_data = cursor.fetchall()
    return retrieved_data


# Executes a given query with their values. For example, when inserting data into the database.
def execute_query(query, values):
    if not cnx.is_connected():
        cnx.reconnect()
    cursor.execute(query, values)
    cnx.commit()


#  All the queries made into a dictionary to maintain a nice overview for all the functions above.
sqlQueries = {
      "update_user": """
      INSERT INTO user(id, name, discriminator)
      VALUES (%(user_id)s, %(name)s, %(discriminator)s)
      ON DUPLICATE KEY UPDATE name = %(name)s, discriminator = %(discriminator)s;
      """,
      "update_guild": """
      INSERT INTO guild(id, name, icon, left_at)
      VALUES (%(guild_id)s, %(name)s, %(icon)s, %(left_at)s)
      ON DUPLICATE KEY UPDATE name = %(name)s, icon = %(icon)s, left_at = %(left_at)s;
      """,
      "transaction": """
      INSERT INTO transaction(user_id, guild_id, amount)
      VALUES (%s, %s, %s);
      """,
      "boardgame_action": """
      INSERT INTO boardgame_action(game, user_id, guild_id, wld)
      VALUES (%s, %s, %s, %s);
      """,
      "get_balance": """
      SELECT money, ranks FROM balance WHERE user_id = %s;
      """,
      "get_games": """
      SELECT DISTINCT game
      FROM boardgame_action;
      """,
      "get_stats": """
      SELECT *
      FROM    
         (SELECT *, rank() over (ORDER BY score DESC) as ranks
         FROM stats
         WHERE game like %s
         ) as topstats
      WHERE user_id = %s
      """,
      "total_boardgame_stats": """
      SELECT *
      FROM total_boardgame_stats
      WHERE user_id = %s;
      """,
      "top_balance": """
      SELECT name, money, users, user_id, discriminator, ranks
      FROM user, balance, (SELECT count(*) as users FROM balance) as users
      WHERE user.id = balance.user_id
      ORDER BY money DESC
      LIMIT 10
      OFFSET %s;""",
      "top_boardgame": """
      SELECT user_id, name, discriminator, wins, losses, draws, score, users, ranks
      FROM user, total_boardgame_stats, (SELECT count(*) as users FROM total_boardgame_stats) as users
      WHERE user.id = total_boardgame_stats.user_id
      ORDER BY score DESC
      LIMIT 10
      OFFSET %s;
      """,
      "app_topbal": """
      SELECT name, money, user_id, discriminator, ranks
      FROM user, balance
      WHERE user.id = balance.user_id
      ORDER BY money DESC
      """,
      "app_topboardgame": """
      SELECT user_id, name, discriminator, wins, losses, draws, score, ranks
      FROM user, total_boardgame_stats
      WHERE user.id = total_boardgame_stats.user_id
      ORDER BY score DESC
      """,
      "search_names": """
      SELECT id, name, discriminator
      FROM user
      WHERE name like %s;
      """,
      "get_user": """
      SELECT id, name, discriminator
      FROM user
      WHERE id = %s
      """
}
