INSERT INTO user(id, name, discriminator)
VALUES (%(user_id)s, %(name)s, %(discriminator)s)
ON DUPLICATE KEY UPDATE name = %(name)s, discriminator = %(discriminator)s;

INSERT INTO guild(id, name, icon, left_at)
VALUES (%(guild_id)s, %(name)s, %(icon)s, %(left_at)s)
ON DUPLICATE KEY UPDATE name = %(name)s, icon = %(icon)s, left_at = %(left_at)s;

INSERT INTO transaction(user_id, guild_id, amount)
VALUES (%s, %s, %s);

INSERT INTO boardgame_action(game, user_id, guild_id, wld)
VALUES (%s, %s, %s, %s);

SELECT money FROM balance WHERE user_id = %s;

SELECT * FROM stats WHERE user_id = %s;

SELECT count(*)
FROM (SELECT DISTINCT money from balance) as money
WHERE money > (
   SELECT money
   FROM balance
   WHERE user_id = %s
);

SELECT count(*)
FROM (SELECT DISTINCT score from (SELECT * FROM stats WHERE game like %(game)s) as g) as score
WHERE score > (
   SELECT score
   FROM (SELECT DISTINCT * from (SELECT * FROM stats WHERE game like %(game)s) as g) as score
   WHERE user_id = %(user_id)s
);

SELECT *
FROM total_boardgame_stats
WHERE user_id = %s;

SELECT count(*)
FROM (SELECT DISTINCT score FROM total_boardgame_stats) as score
WHERE score > (
   SELECT score
   FROM total_boardgame_stats
   WHERE user_id = %s
);

SELECT name, money, users, user_id, discriminator
FROM user, balance, (SELECT count(*) as users FROM balance) as users
WHERE user.id = balance.user_id
ORDER BY money DESC
LIMIT 10
OFFSET %s;

SELECT user_id, name, discriminator, wins, losses, draws, score, users
FROM user, total_boardgame_stats, (SELECT count(*) as users FROM total_boardgame_stats) as users
WHERE user.id = total_boardgame_stats.user_id
ORDER BY score DESC
LIMIT 10
OFFSET %s;