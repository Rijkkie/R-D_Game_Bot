-- MySQL dump 10.13  Distrib 8.0.25, for Linux (x86_64)
--
-- Host: localhost    Database: gamebot
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `balance`
--

DROP TABLE IF EXISTS `balance`;
/*!50001 DROP VIEW IF EXISTS `balance`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `balance` AS SELECT 
 1 AS `user_id`,
 1 AS `money`,
 1 AS `ranks`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `boardgame_action`
--

DROP TABLE IF EXISTS `boardgame_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boardgame_action` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `game` varchar(80) NOT NULL,
  `user_id` bigint unsigned NOT NULL,
  `guild_id` bigint unsigned NOT NULL,
  `wld` char(1) NOT NULL,
  `creation_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fkIdx_111` (`guild_id`),
  KEY `fkIdx_65` (`user_id`),
  CONSTRAINT `FK_110` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`),
  CONSTRAINT `FK_64` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `wld_value` CHECK (((`wld` = _utf8mb4'w') or (`wld` = _utf8mb4'l') or (`wld` = _utf8mb4'd')))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `guild`
--

DROP TABLE IF EXISTS `guild`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guild` (
  `id` bigint unsigned NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `joined_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `left_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `stats`
--

DROP TABLE IF EXISTS `stats`;
/*!50001 DROP VIEW IF EXISTS `stats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `stats` AS SELECT 
 1 AS `game`,
 1 AS `user_id`,
 1 AS `wins`,
 1 AS `losses`,
 1 AS `draws`,
 1 AS `score`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `total_boardgame_stats`
--

DROP TABLE IF EXISTS `total_boardgame_stats`;
/*!50001 DROP VIEW IF EXISTS `total_boardgame_stats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `total_boardgame_stats` AS SELECT 
 1 AS `user_id`,
 1 AS `wins`,
 1 AS `losses`,
 1 AS `draws`,
 1 AS `score`,
 1 AS `ranks`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `guild_id` bigint unsigned NOT NULL,
  `user_id` bigint unsigned NOT NULL,
  `amount` bigint NOT NULL,
  `creation_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `guild_id` (`guild_id`),
  KEY `fkIdx_89` (`user_id`),
  CONSTRAINT `FK_88` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `transaction_ibfk_1` FOREIGN KEY (`guild_id`) REFERENCES `guild` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint unsigned NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `discriminator` varchar(4) DEFAULT NULL,
  `joined_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Final view structure for view `balance`
--

/*!50001 DROP VIEW IF EXISTS `balance`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`totti`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `balance` AS select `balance`.`user_id` AS `user_id`,`balance`.`money` AS `money`,rank() OVER (ORDER BY `balance`.`money` desc )  AS `ranks` from (select `transaction`.`user_id` AS `user_id`,(sum(`transaction`.`amount`) + 100) AS `money` from `transaction` group by `transaction`.`user_id` union select `user`.`id` AS `id`,100 AS `money` from `user` where exists(select 1 from `transaction` where (`transaction`.`user_id` = `user`.`id`)) is false) `balance` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `stats`
--

/*!50001 DROP VIEW IF EXISTS `stats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`totti`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `stats` AS select `wins`.`game` AS `game`,`wins`.`user_id` AS `user_id`,`wins`.`wins` AS `wins`,`losses`.`losses` AS `losses`,`draws`.`draws` AS `draws`,(((`wins`.`wins` * 100) + (`losses`.`losses` * 10)) + (`draws`.`draws` * 50)) AS `score` from (((select `a1`.`game` AS `game`,`a1`.`user_id` AS `user_id`,count(0) AS `wins` from (`boardgame_action` `a1` join `boardgame_action` `a2`) where ((`a1`.`id` = `a2`.`id`) and (`a1`.`wld` = 'w')) group by `a1`.`game`,`a1`.`user_id` union select `all_games`.`game` AS `game`,`user`.`id` AS `user_id`,0 AS `wins` from ((select distinct `boardgame_action`.`game` AS `game` from `boardgame_action`) `all_games` join `user`) where (`all_games`.`game`,`user`.`id`) in (select `boardgame_action`.`game`,`boardgame_action`.`user_id` from `boardgame_action` where (`boardgame_action`.`wld` = 'w')) is false) `wins` join (select `a1`.`game` AS `game`,`a1`.`user_id` AS `user_id`,count(0) AS `losses` from (`boardgame_action` `a1` join `boardgame_action` `a2`) where ((`a1`.`id` = `a2`.`id`) and (`a1`.`wld` = 'l')) group by `a1`.`game`,`a1`.`user_id` union select `all_games`.`game` AS `game`,`user`.`id` AS `user_id`,0 AS `losses` from ((select distinct `boardgame_action`.`game` AS `game` from `boardgame_action`) `all_games` join `user`) where (`all_games`.`game`,`user`.`id`) in (select `boardgame_action`.`game`,`boardgame_action`.`user_id` from `boardgame_action` where (`boardgame_action`.`wld` = 'l')) is false) `losses`) join (select `a1`.`game` AS `game`,`a1`.`user_id` AS `user_id`,count(0) AS `draws` from (`boardgame_action` `a1` join `boardgame_action` `a2`) where ((`a1`.`id` = `a2`.`id`) and (`a1`.`wld` = 'd')) group by `a1`.`game`,`a1`.`user_id` union select `all_games`.`game` AS `game`,`user`.`id` AS `user_id`,0 AS `draws` from ((select distinct `boardgame_action`.`game` AS `game` from `boardgame_action`) `all_games` join `user`) where (`all_games`.`game`,`user`.`id`) in (select `boardgame_action`.`game`,`boardgame_action`.`user_id` from `boardgame_action` where (`boardgame_action`.`wld` = 'd')) is false) `draws`) where ((`wins`.`user_id` = `losses`.`user_id`) and (`losses`.`user_id` = `draws`.`user_id`) and (`wins`.`game` = `losses`.`game`) and (`losses`.`game` = `draws`.`game`)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `total_boardgame_stats`
--

/*!50001 DROP VIEW IF EXISTS `total_boardgame_stats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`totti`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `total_boardgame_stats` AS select `total_boardgame_stats`.`user_id` AS `user_id`,`total_boardgame_stats`.`wins` AS `wins`,`total_boardgame_stats`.`losses` AS `losses`,`total_boardgame_stats`.`draws` AS `draws`,`total_boardgame_stats`.`score` AS `score`,rank() OVER (ORDER BY `total_boardgame_stats`.`score` desc )  AS `ranks` from (select `stats`.`user_id` AS `user_id`,sum(`stats`.`wins`) AS `wins`,sum(`stats`.`losses`) AS `losses`,sum(`stats`.`draws`) AS `draws`,sum(`stats`.`score`) AS `score` from `stats` group by `stats`.`user_id`) `total_boardgame_stats` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-04 22:59:24
