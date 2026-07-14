CREATE OR REPLACE VIEW `yugioh_db`.`vw_card_tooltip_images_sets` AS
SELECT 
    `c`.`card_id` AS `card_id`,
    `c`.`name` AS `card_name`,
    `c`.`card_type` AS `card_type`,
    `c`.`archetype` AS `card_archetype`,
    `ci`.`image_id` AS `image_id`,
    `ci`.`image_url` AS `image_url`,
    `ci`.`image_url_small` AS `image_url_small`,
    `ci`.`image_url_cropped` AS `image_url_cropped`,
    `cs`.`set_id` AS `set_id`,
    `cs`.`set_name` AS `set_name`
FROM `yugioh_db`.`cards` `c`
LEFT JOIN `yugioh_db`.`card_images` `ci`
    ON `ci`.`card_id` = `c`.`card_id`
LEFT JOIN `yugioh_db`.`card_sets` `cs`
    ON `cs`.`card_id` = `c`.`card_id`;