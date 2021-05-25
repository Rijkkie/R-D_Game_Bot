--#mysqldump -u root -p database_name > test.sql

--wise to make the user themselves create their own schema
--CREATE SCHEMA gamebot_test;
--USE gamebot_test;

CREATE TABLE IF NOT EXISTS `user`
(
 `id`            bigint unsigned NOT NULL ,
 `name`          varchar(255) DEFAULT NULL ,
 `discriminator` int zerofill DEFAULT NULL ,
 `joined_at`     datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ,
 `updated_at`    datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS `guild`
(
 `id`         bigint unsigned NOT NULL ,
 `name`       varchar(255) DEFAULT NULL ,
 `icon`       varchar(255) DEFAULT NULL ,
 `joined_at`  datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
 `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 `left_at`    datetime DEFAULT NULL ,

PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS `boardgame_action`
(
 `id`            int unsigned NOT NULL AUTO_INCREMENT ,
 `game`          varchar(80) NOT NULL ,
 `user_id`       bigint unsigned NOT NULL ,
 `guild_id`      bigint unsigned NOT NULL ,
 `wld`           char NOT NULL ,
 `creation_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ,

PRIMARY KEY (`id`),
KEY `fkIdx_111` (`guild_id`),
CONSTRAINT `FK_110` FOREIGN KEY `fkIdx_111` (`guild_id`) REFERENCES `guild` (`id`),
KEY `fkIdx_65` (`user_id`),
CONSTRAINT `FK_64` FOREIGN KEY `fkIdx_65` (`user_id`) REFERENCES `user` (`id`),
 CONSTRAINT `wld_value` CHECK ( (wld = 'w') OR (wld = 'l') OR (wld = 'd') )
);


CREATE TABLE IF NOT EXISTS `transaction`
(
 `id`            int unsigned NOT NULL AUTO_INCREMENT ,
 `guild_id`      bigint unsigned NOT NULL,
 `user_id`       bigint unsigned NOT NULL ,
 `amount`        bigint signed NOT NULL ,
 `creation_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ,

PRIMARY KEY (`id`),
FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`),
KEY `fkIdx_89` (`user_id`),
CONSTRAINT `FK_88` FOREIGN KEY `fkIdx_89` (`user_id`) REFERENCES `user` (`id`)
);

CREATE VIEW `stats` AS
SELECT wins.game, wins.user_id, wins, losses, draws,  wins * 100 + losses * 10 + draws * 50 as score
FROM
    (SELECT a1.game, a1.user_id, count(*) as wins
    FROM boardgame_action as a1, boardgame_action as a2
    WHERE a1.id = a2.id and a1.wld = 'w'
    GROUP BY a1.game, a1.user_id
    UNION
    SELECT all_games.game, user.id as user_id, 0 as wins
    FROM (SELECT DISTINCT game FROM boardgame_action) as all_games, user
    WHERE (all_games.game, user.id) NOT IN (
    SELECT game, user_id
    FROM boardgame_action
    WHERE wld = 'w')) AS wins
INNER JOIN
    (SELECT a1.game, a1.user_id, count(*) as losses
    FROM boardgame_action as a1, boardgame_action as a2
    WHERE a1.id = a2.id and a1.wld = 'l'
    GROUP BY a1.game, a1.user_id
    UNION
    SELECT all_games.game, user.id as user_id, 0 as losses
    FROM (SELECT DISTINCT game FROM boardgame_action) as all_games, user
    WHERE (all_games.game, user.id) NOT IN (
    SELECT game, user_id
    FROM boardgame_action
    WHERE wld = 'l')) AS losses
INNER JOIN
    (SELECT a1.game, a1.user_id, count(*) as draws
    FROM boardgame_action as a1, boardgame_action as a2
    WHERE a1.id = a2.id and a1.wld = 'd'
    GROUP BY a1.game, a1.user_id
    UNION
    SELECT all_games.game, user.id as user_id, 0 as draws
    FROM (SELECT DISTINCT game FROM boardgame_action) as all_games, user
    WHERE (all_games.game, user.id) NOT IN (
    SELECT game, user_id
    FROM boardgame_action
    WHERE wld = 'd')) AS draws
WHERE wins.user_id = losses.user_id
AND losses.user_id = draws.user_id
AND wins.game = losses.game
AND losses.game = draws.game;

CREATE VIEW `balance` AS
SELECT user_id, sum(amount) + 1000 as money
FROM transaction
GROUP BY user_id
UNION
SELECT user.id, 1000 as money
FROM user
WHERE not exists(
   SELECT *
   FROM transaction
   WHERE transaction.user_id = user.id);

CREATE VIEW `total_stats` as
SELECT user_id, sum(wins) as wins, sum(losses) as losses, sum(draws) as draws, sum(score) as score
FROM stats
GROUP BY user_id;