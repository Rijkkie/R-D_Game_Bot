--#mysqldump -u root -p database_name > test.sql
--#To do: create view for balance and score.

--wise to make the user themselves create their own schema
--CREATE SCHEMA gamebot_test;
--USE gamebot_test;

CREATE TABLE IF NOT EXISTS `user`
(
 `id`            bigint unsigned NOT NULL ,
 `name`          varchar(255) DEFAULT NULL ,
 `discriminator` int DEFAULT NULL ,
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
 `user_id`       bigint unsigned NOT NULL ,
 `amount`        bigint signed NOT NULL ,
 `creation_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ,

PRIMARY KEY (`id`),
KEY `fkIdx_89` (`user_id`),
CONSTRAINT `FK_88` FOREIGN KEY `fkIdx_89` (`user_id`) REFERENCES `user` (`id`)
);