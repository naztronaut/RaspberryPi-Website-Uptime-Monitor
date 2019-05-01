CREATE DATABASE `uptime`;
USE `uptime`;

CREATE TABLE `activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activityType` varchar(45) NOT NULL,
  `createdAt` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `sitesAffected` longtext,
  PRIMARY KEY (`id`)
);

CREATE TABLE `currentStatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createdAt` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `site` varchar(150) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `site` (`site`)
);

CREATE TABLE `sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siteName` varchar(999) NOT NULL,
  `updatedAt` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `url` varchar(150) DEFAULT NULL,
  `status` varchar(255) DEFAULT 0,
  `active` int(1) DEFAULT 1,
  `email` varchar(999) DEFAULT NULL,
  `visible` int(1) DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
);


CREATE TABLE `outages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createdAt` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `sitesAffected` longtext,
  `numberOfSites` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
);

CREATE TABLE `downtimeCounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `site` varchar(150) DEFAULT NULL,
  `downCount` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniqueSite` (`site`)
);

CREATE TABLE `cronSettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment` varchar(150) NOT NULL,
  `updateDate` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `cronName` varchar(500) DEFAULT NULL,
  `cronVal` int(11) DEFAULT NULL,
  `cronScript` varchar(250) DEFAULT NULL,
  `enabled` tinyint(2) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment` (`comment`)
);

CREATE TABLE `ledStatus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `color` varchar(150) DEFAULT NULL,
  `pin` int(3) DEFAULT NULL,
  `updateDate` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `status` tinyint(2) DEFAULT NULL,
  `active` tinyint(2) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
);

-- Inserts the three LED pins and preliminary status
INSERT INTO ledStatus (color, pin, status) VALUES ('red', 18, 0),('yellow',25,0),('green',12,0);


-- Store emails that were sent out
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `createdAt` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `content` longtext,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_unique` (`id`)
);


-- Archive tables --

 CREATE TABLE `archive_downtimeCounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `site` varchar(150) DEFAULT NULL,
  `downCount` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
)