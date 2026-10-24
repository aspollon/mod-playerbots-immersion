-- City Life: remove the quest hubs of the former quest system.
-- The normal Playerbots now do the questing; the city hubs stay untouched.

DELETE `spot` FROM `city_life_spot` AS `spot`
INNER JOIN `city_life_hub` AS `hub` ON `hub`.`id` = `spot`.`hub_id`
WHERE `hub`.`name` LIKE '%Questing';

DELETE FROM `city_life_hub` WHERE `name` LIKE '%Questing';
