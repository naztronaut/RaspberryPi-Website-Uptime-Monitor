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
