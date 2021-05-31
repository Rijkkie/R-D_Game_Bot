import mysql.connector as mysql
import json

with open("./config.json") as config_file:
    config = json.load(config_file)
cnx = mysql.connect(**config["mysql"])
cursor = cnx.cursor()

# I was not really sure if I should have separated the queries from the functions and place them in queries.sql or not
# Because it made the overview of the functions a lot cleaner.
# Instead of separating the queries to queries.sql, I decided to create a dictionary instead.
# Removed this piece of code and replaced it with a dictionary of queries at the bottom of this file.
# sqlFile = open('database/dbscripts/queries.sql', 'r')
# sqlQueries = sqlFile.read().split(';')
# sqlFile.close()

# The view 'balance' has a standard money value for every user (1000) that is implemented on the database,
# The same goes for the view 'stats' with 100 points per win, 50 per draw and 10 per loss.
# Change the values in dbtables.sql and drop the tables and


# Whenever this function is called, it will create the database and tables if they did not already exist.
def db_startup():
    sql_file = open('database/dbscripts/dbtables.sql', 'r')
    sql_queries = sql_file.read().split(';')
    cursor.execute("CREATE SCHEMA IF NOT EXISTS `" + config["database_name"] + "`")
    cursor.execute("USE " + config["database_name"])
    for query in sql_queries:
        cursor.execute(query)
    cnx.commit()


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
def get_stats(user_id):
    return retrieve_query(sqlQueries["get_stats"], (user_id,))


# Used to retrieve the stats rank of a specific user and specific game.
def stats_rank(game, user_id):
    values = {'game': game, 'user_id': user_id}
    count = retrieve_query(sqlQueries["stats_rank"], values)[0][0]
    return 1 if (count == 0) else count + 1


# Used to retrieve the sum of the boardgame stats and their rank of a specific user.
def total_boardgame_stats(user_id):
    return retrieve_query(sqlQueries["total_boardgame_stats"], (user_id,))


# Used to retrieve a leaderboard page of the global balances in descending order.
def top_balance(offset):
    return retrieve_query(sqlQueries["top_balance"], (offset,))


# Used to retrieve a leaderboard page of the global stats in descending order.
def top_boardgame(offset):
    return retrieve_query(sqlQueries["top_boardgame"], (offset,))


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
      "get_stats": """
      SELECT * FROM stats WHERE user_id = %s;
      """,
      "stats_rank": """
      SELECT count(*)
      FROM (SELECT DISTINCT score from (SELECT * FROM stats WHERE game like %(game)s) as g) as score
      WHERE score > (
        SELECT score
        FROM (SELECT DISTINCT * from (SELECT * FROM stats WHERE game like %(game)s) as g) as score
        WHERE user_id = %(user_id)s
        );
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
      """
}
