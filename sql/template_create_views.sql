-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: yugioh_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Temporary view structure for view `vw_card_tooltip_images_sets`
--

DROP TABLE IF EXISTS `vw_card_tooltip_images_sets`;
/*!50001 DROP VIEW IF EXISTS `vw_card_tooltip_images_sets`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_card_tooltip_images_sets` AS SELECT 
 1 AS `card_id`,
 1 AS `card_name`,
 1 AS `card_type`,
 1 AS `card_archetype`,
 1 AS `image_id`,
 1 AS `image_url`,
 1 AS `image_url_small`,
 1 AS `image_url_cropped`,
 1 AS `set_id`,
 1 AS `set_name`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_dim_cards_descriptive`
--

DROP TABLE IF EXISTS `vw_dim_cards_descriptive`;
/*!50001 DROP VIEW IF EXISTS `vw_dim_cards_descriptive`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_dim_cards_descriptive` AS SELECT 
 1 AS `card_id`,
 1 AS `name`,
 1 AS `card_type`,
 1 AS `human_readable_card_type`,
 1 AS `frame_type`,
 1 AS `race`,
 1 AS `archetype`,
 1 AS `atk`,
 1 AS `def`,
 1 AS `attribute`,
 1 AS `level`,
 1 AS `scale`,
 1 AS `link_value`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_dim_marketplaces_descriptive`
--

DROP TABLE IF EXISTS `vw_dim_marketplaces_descriptive`;
/*!50001 DROP VIEW IF EXISTS `vw_dim_marketplaces_descriptive`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_dim_marketplaces_descriptive` AS SELECT 
 1 AS `marketplace_id`,
 1 AS `marketplace`,
 1 AS `marketplace_name`,
 1 AS `default_currency`,
 1 AS `market_region`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_dim_rarities_descriptive`
--

DROP TABLE IF EXISTS `vw_dim_rarities_descriptive`;
/*!50001 DROP VIEW IF EXISTS `vw_dim_rarities_descriptive`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_dim_rarities_descriptive` AS SELECT 
 1 AS `rarity_id`,
 1 AS `set_code`,
 1 AS `rarity_name`,
 1 AS `rarity_code`,
 1 AS `rarity_business_key`,
 1 AS `created_at`,
 1 AS `updated_at`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_dim_sets_descriptive`
--

DROP TABLE IF EXISTS `vw_dim_sets_descriptive`;
/*!50001 DROP VIEW IF EXISTS `vw_dim_sets_descriptive`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_dim_sets_descriptive` AS SELECT 
 1 AS `set_id`,
 1 AS `set_name`,
 1 AS `created_at`,
 1 AS `updated_at`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_dim_snapshots_descriptive`
--

DROP TABLE IF EXISTS `vw_dim_snapshots_descriptive`;
/*!50001 DROP VIEW IF EXISTS `vw_dim_snapshots_descriptive`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_dim_snapshots_descriptive` AS SELECT 
 1 AS `snapshot_at`,
 1 AS `snapshot_date`,
 1 AS `snapshot_year`,
 1 AS `snapshot_quarter`,
 1 AS `snapshot_month`,
 1 AS `snapshot_month_name`,
 1 AS `snapshot_day`,
 1 AS `snapshot_hour`,
 1 AS `snapshot_day_of_week`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_fact_avg_market_price`
--

DROP TABLE IF EXISTS `vw_fact_avg_market_price`;
/*!50001 DROP VIEW IF EXISTS `vw_fact_avg_market_price`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_fact_avg_market_price` AS SELECT 
 1 AS `card_id`,
 1 AS `card_name`,
 1 AS `cardmarket`,
 1 AS `tcgplayer`,
 1 AS `ebay`,
 1 AS `amazon`,
 1 AS `coolstuffinc`,
 1 AS `avg_price_USD`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_fact_card_price_variation_predictive`
--

DROP TABLE IF EXISTS `vw_fact_card_price_variation_predictive`;
/*!50001 DROP VIEW IF EXISTS `vw_fact_card_price_variation_predictive`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_fact_card_price_variation_predictive` AS SELECT 
 1 AS `card_id`,
 1 AS `card_name`,
 1 AS `marketplace`,
 1 AS `currency`,
 1 AS `snapshot_at`,
 1 AS `previous_snapshot_at`,
 1 AS `days_between_snapshots`,
 1 AS `price`,
 1 AS `previous_price`,
 1 AS `price_change`,
 1 AS `price_change_pct`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_fact_card_prices_descriptive`
--

DROP TABLE IF EXISTS `vw_fact_card_prices_descriptive`;
/*!50001 DROP VIEW IF EXISTS `vw_fact_card_prices_descriptive`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_fact_card_prices_descriptive` AS SELECT 
 1 AS `card_id`,
 1 AS `card_name`,
 1 AS `marketplace`,
 1 AS `currency`,
 1 AS `price`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vw_fact_card_set_appearances`
--

DROP TABLE IF EXISTS `vw_fact_card_set_appearances`;
/*!50001 DROP VIEW IF EXISTS `vw_fact_card_set_appearances`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_fact_card_set_appearances` AS SELECT 
 1 AS `card_set_appearance_id`,
 1 AS `card_id`,
 1 AS `card_name`,
 1 AS `set_id`,
 1 AS `set_name`,
 1 AS `rarity_id`,
 1 AS `rarity_name`,
 1 AS `rarity_code`,
 1 AS `set_code`,
 1 AS `set_price`,
 1 AS `appearance_count`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vw_card_tooltip_images_sets`
--

/*!50001 DROP VIEW IF EXISTS `vw_card_tooltip_images_sets`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_card_tooltip_images_sets` AS select `c`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`c`.`card_type` AS `card_type`,`c`.`archetype` AS `card_archetype`,`ci`.`image_id` AS `image_id`,`ci`.`image_url` AS `image_url`,`ci`.`image_url_small` AS `image_url_small`,`ci`.`image_url_cropped` AS `image_url_cropped`,`cs`.`set_id` AS `set_id`,`cs`.`set_name` AS `set_name` from ((`cards` `c` left join `card_images` `ci` on((`ci`.`card_id` = `c`.`card_id`))) left join `card_sets` `cs` on((`cs`.`card_id` = `c`.`card_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_dim_cards_descriptive`
--

/*!50001 DROP VIEW IF EXISTS `vw_dim_cards_descriptive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_dim_cards_descriptive` AS select `c`.`card_id` AS `card_id`,`c`.`name` AS `name`,`c`.`card_type` AS `card_type`,`c`.`human_readable_card_type` AS `human_readable_card_type`,`c`.`frame_type` AS `frame_type`,`c`.`race` AS `race`,coalesce(`c`.`archetype`,'Sin arquetipo') AS `archetype`,cast(`c`.`atk` as signed) AS `atk`,cast(`c`.`def` as signed) AS `def`,coalesce(`c`.`attribute`,'No aplica') AS `attribute`,cast(`c`.`level` as signed) AS `level`,cast(`c`.`scale` as signed) AS `scale`,cast(`c`.`link_value` as signed) AS `link_value` from `cards` `c` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_dim_marketplaces_descriptive`
--

/*!50001 DROP VIEW IF EXISTS `vw_dim_marketplaces_descriptive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_dim_marketplaces_descriptive` AS select 1 AS `marketplace_id`,'cardmarket' AS `marketplace`,'Cardmarket' AS `marketplace_name`,'EUR' AS `default_currency`,'Europe' AS `market_region` union all select 2 AS `marketplace_id`,'tcgplayer' AS `tcgplayer`,'TCGplayer' AS `TCGplayer`,'USD' AS `USD`,'United States' AS `United States` union all select 3 AS `marketplace_id`,'ebay' AS `ebay`,'eBay' AS `eBay`,'USD' AS `USD`,'Global' AS `Global` union all select 4 AS `marketplace_id`,'amazon' AS `amazon`,'Amazon' AS `Amazon`,'USD' AS `USD`,'Global' AS `Global` union all select 5 AS `marketplace_id`,'coolstuffinc' AS `coolstuffinc`,'CoolStuffInc' AS `CoolStuffInc`,'USD' AS `USD`,'United States' AS `United States` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_dim_rarities_descriptive`
--

/*!50001 DROP VIEW IF EXISTS `vw_dim_rarities_descriptive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_dim_rarities_descriptive` AS select `r`.`id` AS `rarity_id`,`r`.`set_code` AS `set_code`,`r`.`rarity_name` AS `rarity_name`,`r`.`rarity_code` AS `rarity_code`,concat(`r`.`set_code`,'|',`r`.`rarity_name`,'|',`r`.`rarity_code`) AS `rarity_business_key`,`r`.`created_at` AS `created_at`,`r`.`updated_at` AS `updated_at` from `rarities` `r` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_dim_sets_descriptive`
--

/*!50001 DROP VIEW IF EXISTS `vw_dim_sets_descriptive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_dim_sets_descriptive` AS select `s`.`id` AS `set_id`,`s`.`set_name` AS `set_name`,`s`.`created_at` AS `created_at`,`s`.`updated_at` AS `updated_at` from `sets` `s` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_dim_snapshots_descriptive`
--

/*!50001 DROP VIEW IF EXISTS `vw_dim_snapshots_descriptive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_dim_snapshots_descriptive` AS select `cph`.`snapshot_at` AS `snapshot_at`,cast(`cph`.`snapshot_at` as date) AS `snapshot_date`,year(`cph`.`snapshot_at`) AS `snapshot_year`,quarter(`cph`.`snapshot_at`) AS `snapshot_quarter`,month(`cph`.`snapshot_at`) AS `snapshot_month`,monthname(`cph`.`snapshot_at`) AS `snapshot_month_name`,dayofmonth(`cph`.`snapshot_at`) AS `snapshot_day`,hour(`cph`.`snapshot_at`) AS `snapshot_hour`,dayofweek(`cph`.`snapshot_at`) AS `snapshot_day_of_week` from `card_price_history` `cph` group by `cph`.`snapshot_at` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_fact_avg_market_price`
--

/*!50001 DROP VIEW IF EXISTS `vw_fact_avg_market_price`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_fact_avg_market_price` AS with `avg_market_price` as (select `cp`.`card_id` AS `card_id`,`cp`.`cardmarket_price` AS `cardmarket`,`cp`.`tcgplayer_price` AS `tcgplayer`,`cp`.`ebay_price` AS `ebay`,`cp`.`amazon_price` AS `amazon`,`cp`.`coolstuffinc_price` AS `coolstuffinc`,((((coalesce(`cp`.`tcgplayer_price`,0) + coalesce(`cp`.`ebay_price`,0)) + coalesce(`cp`.`amazon_price`,0)) + coalesce(`cp`.`coolstuffinc_price`,0)) / nullif(((((`cp`.`tcgplayer_price` is not null) + (`cp`.`ebay_price` is not null)) + (`cp`.`amazon_price` is not null)) + (`cp`.`coolstuffinc_price` is not null)),0)) AS `avg_price_USD` from `card_prices` `cp`) select `amp`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`amp`.`cardmarket` AS `cardmarket`,`amp`.`tcgplayer` AS `tcgplayer`,`amp`.`ebay` AS `ebay`,`amp`.`amazon` AS `amazon`,`amp`.`coolstuffinc` AS `coolstuffinc`,`amp`.`avg_price_USD` AS `avg_price_USD` from (`avg_market_price` `amp` join `cards` `c` on((`c`.`card_id` = `amp`.`card_id`))) order by `amp`.`avg_price_USD` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_fact_card_price_variation_predictive`
--

/*!50001 DROP VIEW IF EXISTS `vw_fact_card_price_variation_predictive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_fact_card_price_variation_predictive` AS with `price_history_long` as (select `cph`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`cph`.`snapshot_at` AS `snapshot_at`,'cardmarket' AS `marketplace`,'EUR' AS `currency`,`cph`.`cardmarket_price` AS `price` from (`card_price_history` `cph` left join `cards` `c` on((`cph`.`card_id` = `c`.`card_id`))) where (`cph`.`cardmarket_price` is not null) union all select `cph`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`cph`.`snapshot_at` AS `snapshot_at`,'tcgplayer' AS `marketplace`,'USD' AS `currency`,`cph`.`tcgplayer_price` AS `price` from (`card_price_history` `cph` left join `cards` `c` on((`cph`.`card_id` = `c`.`card_id`))) where (`cph`.`tcgplayer_price` is not null) union all select `cph`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`cph`.`snapshot_at` AS `snapshot_at`,'ebay' AS `marketplace`,'USD' AS `currency`,`cph`.`ebay_price` AS `price` from (`card_price_history` `cph` left join `cards` `c` on((`cph`.`card_id` = `c`.`card_id`))) where (`cph`.`ebay_price` is not null) union all select `cph`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`cph`.`snapshot_at` AS `snapshot_at`,'amazon' AS `marketplace`,'USD' AS `currency`,`cph`.`amazon_price` AS `price` from (`card_price_history` `cph` left join `cards` `c` on((`cph`.`card_id` = `c`.`card_id`))) where (`cph`.`amazon_price` is not null) union all select `cph`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`cph`.`snapshot_at` AS `snapshot_at`,'coolstuffinc' AS `marketplace`,'USD' AS `currency`,`cph`.`coolstuffinc_price` AS `price` from (`card_price_history` `cph` left join `cards` `c` on((`cph`.`card_id` = `c`.`card_id`))) where (`cph`.`coolstuffinc_price` is not null)), `price_history_with_previous` as (select `price_history_long`.`card_id` AS `card_id`,`price_history_long`.`card_name` AS `card_name`,`price_history_long`.`marketplace` AS `marketplace`,`price_history_long`.`currency` AS `currency`,`price_history_long`.`snapshot_at` AS `snapshot_at`,`price_history_long`.`price` AS `price`,lag(`price_history_long`.`snapshot_at`) OVER (PARTITION BY `price_history_long`.`card_id`,`price_history_long`.`marketplace`,`price_history_long`.`currency` ORDER BY `price_history_long`.`snapshot_at` )  AS `previous_snapshot_at`,lag(`price_history_long`.`price`) OVER (PARTITION BY `price_history_long`.`card_id`,`price_history_long`.`marketplace`,`price_history_long`.`currency` ORDER BY `price_history_long`.`snapshot_at` )  AS `previous_price` from `price_history_long`) select `price_history_with_previous`.`card_id` AS `card_id`,`price_history_with_previous`.`card_name` AS `card_name`,`price_history_with_previous`.`marketplace` AS `marketplace`,`price_history_with_previous`.`currency` AS `currency`,`price_history_with_previous`.`snapshot_at` AS `snapshot_at`,`price_history_with_previous`.`previous_snapshot_at` AS `previous_snapshot_at`,(to_days(`price_history_with_previous`.`snapshot_at`) - to_days(`price_history_with_previous`.`previous_snapshot_at`)) AS `days_between_snapshots`,`price_history_with_previous`.`price` AS `price`,`price_history_with_previous`.`previous_price` AS `previous_price`,(`price_history_with_previous`.`price` - `price_history_with_previous`.`previous_price`) AS `price_change`,(case when ((`price_history_with_previous`.`previous_price` is null) or (`price_history_with_previous`.`previous_price` = 0)) then NULL else ((`price_history_with_previous`.`price` - `price_history_with_previous`.`previous_price`) / `price_history_with_previous`.`previous_price`) end) AS `price_change_pct` from `price_history_with_previous` where (`price_history_with_previous`.`previous_snapshot_at` is not null) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_fact_card_prices_descriptive`
--

/*!50001 DROP VIEW IF EXISTS `vw_fact_card_prices_descriptive`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_fact_card_prices_descriptive` AS select `c`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,'cardmarket' AS `marketplace`,'EUR' AS `currency`,`cp`.`cardmarket_price` AS `price` from (`card_prices` `cp` left join `cards` `c` on((`cp`.`card_id` = `c`.`card_id`))) where (`cp`.`cardmarket_price` is not null) union all select `c`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,'tcgplayer' AS `marketplace`,'USD' AS `currency`,`cp`.`tcgplayer_price` AS `price` from (`card_prices` `cp` left join `cards` `c` on((`cp`.`card_id` = `c`.`card_id`))) where (`cp`.`tcgplayer_price` is not null) union all select `c`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,'ebay' AS `marketplace`,'USD' AS `currency`,`cp`.`ebay_price` AS `price` from (`card_prices` `cp` left join `cards` `c` on((`cp`.`card_id` = `c`.`card_id`))) where (`cp`.`ebay_price` is not null) union all select `c`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,'amazon' AS `marketplace`,'USD' AS `currency`,`cp`.`amazon_price` AS `price` from (`card_prices` `cp` left join `cards` `c` on((`cp`.`card_id` = `c`.`card_id`))) where (`cp`.`amazon_price` is not null) union all select `c`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,'coolstuffinc' AS `marketplace`,'USD' AS `currency`,`cp`.`coolstuffinc_price` AS `price` from (`card_prices` `cp` left join `cards` `c` on((`cp`.`card_id` = `c`.`card_id`))) where (`cp`.`coolstuffinc_price` is not null) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vw_fact_card_set_appearances`
--

/*!50001 DROP VIEW IF EXISTS `vw_fact_card_set_appearances`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`pepin`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_fact_card_set_appearances` AS select `cs`.`id` AS `card_set_appearance_id`,`cs`.`card_id` AS `card_id`,`c`.`name` AS `card_name`,`cs`.`set_id` AS `set_id`,coalesce(`s`.`set_name`,`cs`.`set_name`) AS `set_name`,`cs`.`rarity_id` AS `rarity_id`,coalesce(nullif(`r`.`rarity_name`,''),`cs`.`set_rarity`) AS `rarity_name`,coalesce(nullif(`r`.`rarity_code`,''),`cs`.`set_rarity_code`) AS `rarity_code`,`cs`.`set_code` AS `set_code`,`cs`.`set_price` AS `set_price`,1 AS `appearance_count` from (((`card_sets` `cs` left join `cards` `c` on((`cs`.`card_id` = `c`.`card_id`))) left join `sets` `s` on((`cs`.`set_id` = `s`.`id`))) left join `rarities` `r` on((`cs`.`rarity_id` = `r`.`id`))) */;
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

-- Dump completed on 2026-07-06 10:35:52
