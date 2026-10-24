-- City Life: custom city characters and conversations.
-- Apply manually to WORLD after world_city_life.sql. No CHARACTER or AUTH changes.
-- Additive, rerunnable seed: existing named hubs/spots and chat IDs are preserved.
-- Custom hubs start with database enabled=0 for older binaries. The new Custom config
-- controls them explicitly and enables every bundled role by default.
-- Routine switches, levels, populations and timings belong in the single config.
-- Positions, faction assignments and chat content remain WORLD data.

CREATE TABLE IF NOT EXISTS `city_life_custom_chat` (
  `id` INT UNSIGNED NOT NULL,
  `group_name` VARCHAR(40) NOT NULL,
  `conversation_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `step` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `speaker_team` TINYINT UNSIGNED NOT NULL DEFAULT 2 COMMENT '0=Alliance,1=Horde,2=Any',
  `channel` TINYINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '0=say,1=yell',
  `text` VARCHAR(255) NOT NULL,
  `weight` INT UNSIGNED NOT NULL DEFAULT 100,
  `enabled` TINYINT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  KEY `idx_city_life_custom_chat_group` (`group_name`,`enabled`,`conversation_id`,`step`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO `city_life_hub`
(`name`,`enabled`,`team`,`min_level`,`max_level`,`map_id`,`default_population`,`priority`)
VALUES
('CustomLegendaryStormwind',0,0,80,80,0,1,350),
('CustomLegendaryOrgrimmar',0,1,80,80,1,1,350),
('CustomLegendaryUndercity',0,1,80,80,0,1,350),
('CustomLegendaryDalaran',0,2,80,80,571,1,350),
('CustomBeggarStormwind',0,0,1,1,0,1,350),
('CustomBeggarOrgrimmar',0,1,1,1,1,1,350),
('CustomBuyerStormwind',0,0,1,80,0,1,350),
('CustomBuyerOrgrimmar',0,1,1,80,1,1,350),
('CustomBuyerDalaran',0,2,1,80,571,1,350),
('CustomTrainingDummyStormwind',0,0,80,80,0,1,350),
('CustomTrainingDummyOrgrimmar',0,1,80,80,1,1,350),
('CustomFishingStormwind',0,0,1,80,0,1,350),
('CustomFishingOrgrimmar',0,1,1,80,1,1,350),
('CustomFishingDalaran',0,2,1,80,571,1,350);

-- Stormwind Legendary plaza anchor: in-game GM GPS, map 0, phase 1; captured 2026-10-21.
-- All Legendary slots use the recorded facing. Other plaza anchors use game_tele entries
-- 1276 (ValleyOfStrength) and 1740 (TheEventide). Service anchors reuse the bundled spots.
-- Orgrimmar beggar anchor: creature GUID 12876, entry 16255.
-- Dalaran buyer anchor: creature GUID 117742, entry 29156.
-- Training stands are 2.5 / 2 yards from existing entry 31144 training dummies:
-- Stormwind creature GUID 201239, Orgrimmar creature GUID 202721.
-- No Dalaran training site is seeded: the local base data contains no city dummy there.
-- Fishing anchors use fishing trainers on land beside their respective fishing areas:
-- Stormwind GUID 79836 / entry 5493; Orgrimmar GUID 4673 / entry 3332;
-- Dalaran GUID 102399 / entry 28742. Runtime ground/water checks still apply.
-- The Stormwind fishing anchor is shifted 3 yards sideways from Arnold Leland to leave him clear.
-- Small radii spread multiple bots without forcing a path across a wall or into water.
INSERT IGNORE INTO `city_life_spot`
(`hub_id`,`name`,`category`,`enabled`,`x`,`y`,`z`,`o`,`radius`,`weight`)
SELECT `hub`.`id`,`seed`.`spot_name`,`seed`.`category`,1,`seed`.`x`,`seed`.`y`,
       `seed`.`z`,`seed`.`o`,`seed`.`radius`,`seed`.`weight`
FROM `city_life_hub` AS `hub`
INNER JOIN
(
  SELECT 'CustomLegendaryStormwind' AS `hub_name`,'CustomAnchor' AS `spot_name`,'legendary' AS `category`,
         -8824.208 AS `x`,628.28284 AS `y`,93.914894 AS `z`,3.7331078 AS `o`,5 AS `radius`,100 AS `weight`
  UNION ALL SELECT 'CustomLegendaryOrgrimmar','CustomAnchor','legendary',1548.05,-4417.19,9.50517,0.139761,5,100
  UNION ALL SELECT 'CustomLegendaryUndercity','CustomAnchor','legendary',1584.14,240.308,-52.1534,0.041793,5,100
  UNION ALL SELECT 'CustomLegendaryDalaran','CustomAnchor','legendary',5700.25,641.774,646.28,3.51554,4,100
  UNION ALL SELECT 'CustomBeggarStormwind','CustomAnchor','beggar',-8861.5,636.744,96.1785,1.91113,3,100
  UNION ALL SELECT 'CustomBeggarOrgrimmar','CustomAnchor','beggar',1584.58,-4416.35,8.29802,3.38594,3,100
  UNION ALL SELECT 'CustomBuyerStormwind','CustomAnchor','buyer',-8821.53,659.886,97.4645,0.401426,3,100
  UNION ALL SELECT 'CustomBuyerOrgrimmar','CustomAnchor','buyer',1592.8,-4397.05,7.46388,0.139626,3,100
  UNION ALL SELECT 'CustomBuyerDalaran','CustomAnchor','buyer',5808.13,585.193,652.463,4.7822,3,100
  UNION ALL SELECT 'CustomTrainingDummyStormwind','CustomAnchor','trainingdummy',-8792.94,362.239,101.102,3.141593,1,100
  UNION ALL SELECT 'CustomTrainingDummyOrgrimmar','CustomAnchor','trainingdummy',2001.31,-4839.54,51.959,0,0.75,100
  UNION ALL SELECT 'CustomFishingStormwind','CustomAnchor','fishing',-8799.571827,767.567690,96.4213,1.6057,1,100
  UNION ALL SELECT 'CustomFishingOrgrimmar','CustomAnchor','fishing',2000.62,-4659.66,26.7387,5.3058,1,100
  UNION ALL SELECT 'CustomFishingDalaran','CustomAnchor','fishing',5707.31,612.214,646.791,1.69297,1,100
) AS `seed` ON `seed`.`hub_name`=`hub`.`name`;

-- Ambient role advertisements are flavor text; they do not create a trade or spend gold.
-- Conversation steps 0/1/2 form one complete question/reply/thanks exchange.
INSERT IGNORE INTO `city_life_custom_chat`
(`id`,`group_name`,`conversation_id`,`step`,`speaker_team`,`channel`,`text`,`weight`,`enabled`)
VALUES
(1001,'beggar',0,0,2,0,'pls gold :(',100,1),
(1002,'beggar',0,0,2,0,'Spare a little gold for a fresh adventurer?',100,1),
(1003,'beggar',0,0,2,0,'10g trade and I will give you a private dance!',100,1),
(1004,'beggar',0,0,2,0,'Saving for my first mount. Every copper helps!',100,1),
(1005,'beggar',0,0,2,0,'Lost my shirt at the auction house. Literally.',100,1),
(1006,'beggar',0,0,2,0,'Does anyone have a spare bag? Mine is mostly air.',100,1),
(2001,'buyer',0,0,2,0,'WTB level 55-60 green gear, 10g each!',100,1),
(2002,'buyer',0,0,2,0,'Buying level 55-60 greens for 10 gold. Check your bags!',100,1),
(2003,'buyer',0,0,2,0,'Got spare endgame greens? Offering 10g each!',100,1),
(2004,'buyer',0,0,2,0,'WTB green level 55-60 gear. 10g per item!',100,1),
(3001,'fishing',0,0,2,0,'Still no turtle...',100,1),
(3002,'fishing',0,0,2,0,'Just one more cast.',100,1),
(3003,'fishing',0,0,2,0,'The fish are winning today.',100,1),
(3004,'fishing',0,0,2,0,'Anyone else catching nothing but junk?',100,1),
(3005,'fishing',0,0,2,0,'A quiet spot and a fishing pole. Perfect.',100,1),
(10010,'conversation',1,0,2,0,'Where is the riding trainer?',100,1),
(10011,'conversation',1,1,2,0,'Ask a guard; they can mark the trainer on your map.',100,1),
(10012,'conversation',1,2,2,0,'Thanks! My feet will appreciate it.',100,1),
(10020,'conversation',2,0,2,0,'Have you seen the prices at the auction house?',100,1),
(10021,'conversation',2,1,2,0,'I looked once. My wallet is still recovering.',100,1),
(10022,'conversation',2,2,2,0,'Maybe I will farm it myself after all.',100,1),
(10030,'conversation',3,0,2,0,'How is the fishing today?',100,1),
(10031,'conversation',3,1,2,0,'Mostly patience, with a little fish on the side.',100,1),
(10032,'conversation',3,2,2,0,'Sounds about right. Good luck!',100,1),
(10040,'conversation',4,0,2,0,'That mount looks amazing!',100,1),
(10041,'conversation',4,1,2,0,'Thanks! It took quite a while to get.',100,1),
(10042,'conversation',4,2,2,0,'Worth it. Safe travels!',100,1),
(10050,'conversation',5,0,2,0,'Do you know a good place to repair?',100,1),
(10051,'conversation',5,1,2,0,'One of the nearby equipment vendors should help.',100,1),
(10052,'conversation',5,2,2,0,'Cheers, my armor has seen better days.',100,1),
(10060,'conversation',6,0,2,0,'Ready for another adventure?',100,1),
(10061,'conversation',6,1,2,0,'After I clear some space in these bags.',100,1),
(10062,'conversation',6,2,2,0,'Same problem here. See you at the bank!',100,1);

-- Ambient lines of the Legendary residents (group 'legendary'). Additive and rerunnable.
INSERT IGNORE INTO `city_life_custom_chat`
(`id`,`group_name`,`speaker_team`,`channel`,`text`,`weight`,`enabled`) VALUES
(11001,'legendary',2,0,'You there. Have you seen a worthy opponent lately?',100,1),
(11002,'legendary',2,0,'This armor has seen more battles than you have years.',100,1),
(11003,'legendary',2,0,'The auction house is busy today. Good. Let them fight over copper.',100,1),
(11004,'legendary',2,0,'I remember when this city was still a handful of tents.',100,1),
(11005,'legendary',2,0,'A hero is only as good as the people who keep the city standing.',100,1),
(11006,'legendary',2,0,'If you are looking for trouble, you are looking in the right place.',100,1),
(11007,'legendary',2,0,'My guild has seen worse wars than this. Much worse.',100,1),
(11008,'legendary',2,0,'You can learn a lot by watching the square. Most of it is not flattering.',100,1),
(11009,'legendary',2,0,'Sharp blade, full purse, clear head. In that order.',100,1),
(11010,'legendary',2,0,'The young ones rush in. The old ones walk out again.',100,1),
(11011,'legendary',2,0,'Rest while you can. The road north is long.',100,1),
(11012,'legendary',2,0,'I have earned these scars. I intend to keep them.',100,1);

-- Feles Noctis and SimpleGekAce are the realm's long-suffering beta testers. These lines are
-- spoken in addition to the normal 'legendary' lines, selected by the character name in CityLife.
INSERT IGNORE INTO `city_life_custom_chat`
(`id`,`group_name`,`speaker_team`,`channel`,`text`,`weight`,`enabled`) VALUES
(11101,'legendary_feles',1,0,'I have tested every module on this realm. My reward is a bag of bug reports and two bandages.',100,1),
(11102,'legendary_feles',1,0,'They said "play AFK Realm, it is relaxing". I have not relaxed since the first patch.',100,1),
(11103,'legendary_feles',1,0,'Every morning brings a new update. Every evening brings a new bug. Every night brings another bug report.',100,1),
(11104,'legendary_feles',1,0,'I reported a bug in the auction module. Now the auction house sends me invoices for the investigation.',100,1),
(11105,'legendary_feles',1,0,'The patch notes said "minor fixes". My entire character sheet disagrees.',100,1),
(11106,'legendary_feles',1,0,'I have used /bug so often that the command now greets me by name.',100,1),
(11107,'legendary_feles',1,0,'AFK Realm: play less, report more. Much more. Preferably before breakfast.',100,1),
(11108,'legendary_feles',1,0,'They gave me the title "Legendary Beta Tester". The pay is exposure and a free headache.',100,1),
(11109,'legendary_feles',1,0,'I used to go on adventures. Now I refresh the changelog and wait for the rollback.',100,1),
(11110,'legendary_feles',1,0,'If you see a bug, report it. I need the company.',100,1),
(11111,'legendary_feles',1,0,'My bags are full of herbs, bandages and unresolved tickets.',100,1),
(11112,'legendary_feles',1,0,'The update broke my favorite feature. They fixed it by removing it from the patch notes.',100,1),
(11113,'legendary_feles',1,0,'I am not AFK. I am waiting for the next hotfix.',100,1),
(11114,'legendary_feles',1,0,'The realm is stable. That is what we tell the players, and sometimes the developers.',100,1),
(11115,'legendary_feles',1,0,'I have seen the code. I have also seen the light. The light was a rollback.',100,1),
(11201,'legendary_simplegeekace',1,0,'I am a Paladin. My sacred duty is testing other people''s patches.',100,1),
(11202,'legendary_simplegeekace',1,0,'The Light guides me. Unfortunately, it guides me straight into another bug report.',100,1),
(11203,'legendary_simplegeekace',1,0,'Daily updates? More like daily surprises with worse loot.',100,1),
(11204,'legendary_simplegeekace',1,0,'I have healed through raids. Nothing prepared me for the AFK Realm issue tracker.',100,1),
(11205,'legendary_simplegeekace',1,0,'My beta tester badge is the only item on this realm that never gets nerfed.',100,1),
(11206,'legendary_simplegeekace',1,0,'They said "test the new module". I asked which one. They said "yes".',100,1),
(11207,'legendary_simplegeekace',1,0,'I have read more changelogs than combat logs.',100,1),
(11208,'legendary_simplegeekace',1,0,'The server is fine. The server is fine. The server is fine.',100,1),
(11209,'legendary_simplegeekace',1,0,'I reported a crash. They shipped a new one with it.',100,1),
(11210,'legendary_simplegeekace',1,0,'Every update: two steps forward, one step back, three steps sideways into a wall.',100,1),
(11211,'legendary_simplegeekace',1,0,'I have a holy shield. It does not protect against patch notes.',100,1),
(11212,'legendary_simplegeekace',1,0,'My DPS is low, but my bug reports are mythic quality.',100,1),
(11213,'legendary_simplegeekace',1,0,'AFK Realm is a lifestyle. Mostly the "waiting for a fix" part.',100,1),
(11214,'legendary_simplegeekace',1,0,'I used to play for fun. Now I play for regression testing.',100,1),
(11215,'legendary_simplegeekace',1,0,'The good news: the bug is fixed. The bad news: it was replaced by a bigger one.',100,1),
(11216,'legendary_simplegeekace',1,0,'They call it a hotfix. I call it a new feature nobody asked for.',100,1),
(11217,'legendary_simplegeekace',1,0,'My beta tester contract says "occasional testing". It is a very flexible word.',100,1),
(11218,'legendary_simplegeekace',1,0,'I have seen the future. It has a changelog entry and no explanation.',100,1),
(11219,'legendary_simplegeekace',1,0,'Every module works perfectly. On my machine. In a dream. Before the last update.',100,1),
(11220,'legendary_simplegeekace',1,0,'I have a guild bank tab full of screenshots proving it worked yesterday.',100,1);