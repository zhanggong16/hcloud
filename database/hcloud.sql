-- MySQL dump 10.13  Distrib 5.7.21, for linux-glibc2.12 (x86_64)
--
-- Host: localhost    Database: hcloud
-- ------------------------------------------------------
-- Server version	5.7.21-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `hcloud`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `hcloud` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;

USE `hcloud`;

--
-- Table structure for table `alert_rules`
--

DROP TABLE IF EXISTS `alert_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alert_rules` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `alert_rules_id` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '报警规则ID，自动生成',
  `host_id` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '主机唯一ID，自动生成',
  `service` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '监控服务类型，host，mysql等',
  `monitor_items` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '监控项',
  `statistical_period` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '统计周期',
  `statistical_approach` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '统计方法',
  `compute_mode` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '计算方式',
  `threshold_value` int(4) NOT NULL DEFAULT '0' COMMENT '阈值',
  `deleted` tinyint(1) DEFAULT '0' COMMENT '0未被删除, 1被删除',
  `deleted_time` datetime DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_host_id_service` (`host_id`,`service`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert_rules`
--

LOCK TABLES `alert_rules` WRITE;
/*!40000 ALTER TABLE `alert_rules` DISABLE KEYS */;
/*!40000 ALTER TABLE `alert_rules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `base_dict`
--

DROP TABLE IF EXISTS `base_dict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `base_dict` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `did` tinyint(4) NOT NULL COMMENT '字典id',
  `name` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '字典名称',
  `english_name` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '字典名称-英文',
  `category` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '字典类型',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_did` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `base_dict`
--

LOCK TABLES `base_dict` WRITE;
/*!40000 ALTER TABLE `base_dict` DISABLE KEYS */;
INSERT INTO `base_dict` VALUES (1,0,'linux系统','linux','os_type','2018-03-25 12:48:32','2018-03-25 12:48:32'),(2,1,'windows系统','windows','os_type','2018-03-25 12:48:52','2018-03-25 12:48:52'),(3,0,'未知','unknown','status','2018-03-25 12:49:36','2018-03-25 12:52:45'),(4,1,'正常','running','status','2018-03-25 12:53:03','2018-03-25 12:53:43'),(5,2,'异常','abnormal','status','2018-03-25 12:53:29','2018-03-25 12:54:07'),(6,0,'线上','online','state','2018-03-25 12:54:36','2018-03-25 12:54:36'),(7,1,'下线','offline','state','2018-03-25 12:54:49','2018-03-25 12:55:16'),(8,2,'测试','test','state','2018-03-25 12:55:01','2018-03-25 12:55:01'),(9,0,'云主机','cloud','attribute','2018-03-25 12:55:51','2018-03-25 12:55:51'),(10,1,'物理机','physical','attribute','2018-03-25 12:56:05','2018-03-25 12:56:05'),(11,0,'本地','local','region','2018-03-25 12:56:26','2018-03-25 12:56:26'),(12,0,'固态硬盘','SSD','disk_type','2018-03-25 13:31:00','2018-03-25 13:31:00'),(13,1,'机械硬盘','STAT','disk_type','2018-03-25 13:31:22','2018-03-25 13:31:22');
/*!40000 ALTER TABLE `base_dict` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_pool`
--

DROP TABLE IF EXISTS `host_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_pool` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '主机唯一ID，自动生成',
  `name` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '未命名' COMMENT '实例名称-用户自定义',
  `description` varchar(155) COLLATE utf8_bin NOT NULL DEFAULT '未标注' COMMENT '实例描述-用户自定义',
  `device_key` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '设备唯一key',
  `privateip` varchar(16) COLLATE utf8_bin NOT NULL COMMENT '私网地址，冗余字段',
  `os_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '操作系统类型，Windows/Linux',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '主机运行状态，unknown;running;shutdown',
  `monitor_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '监控状态',
  `state` tinyint(4) NOT NULL DEFAULT '0' COMMENT '主机状态，test;online;offline',
  `attribute` tinyint(4) NOT NULL DEFAULT '0' COMMENT '属性, physical:物理机, cloud:云上',
  `region` tinyint(4) NOT NULL DEFAULT '0' COMMENT '区域',
  `dns` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT 'dns地址',
  `project_id` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '项目id',
  `remark` varchar(155) COLLATE utf8_bin DEFAULT '' COMMENT '备注',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_host_id` (`host_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_pool`
--

LOCK TABLES `host_pool` WRITE;
/*!40000 ALTER TABLE `host_pool` DISABLE KEYS */;
INSERT INTO `host_pool` VALUES (1,'81804888-3027-11e8-9b98-fa163ea5419d','未命名','未标注','','192.168.0.92',0,0,0,0,0,0,'www.hcloud.com','01','','2018-03-25 12:25:41','2018-04-01 09:28:54'),(2,'053c7088-310a-11e8-84ee-ac853dafc5c4','zhanggong','zhanggong ccccc','124124','192.168.1.1',0,0,0,1,0,1,'zhanggong.com','01','','2018-03-26 15:26:34','2018-04-01 15:36:55'),(10,'840bad62-35be-11e8-9bb6-fa163ea5419d','zhanggong','zhanggong mmmmmmmmm','124124','10.10.10.10',1,0,0,1,1,1,'zhanggong.com','01','','2018-04-01 15:08:21','2018-04-01 15:08:21');
/*!40000 ALTER TABLE `host_pool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `host_pool_extend`
--

DROP TABLE IF EXISTS `host_pool_extend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `host_pool_extend` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '主机唯一ID，自动生成',
  `hostname` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '主机hostname',
  `privateip` varchar(16) COLLATE utf8_bin NOT NULL COMMENT '私网地址',
  `privateip_extend` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '私网地址扩展',
  `publicip` varchar(16) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '公网地址',
  `publicip_extend` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '公网地址扩展',
  `cpu_process` tinyint(4) NOT NULL DEFAULT '1' COMMENT '设备cpu核数量',
  `cpu` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '设备cpu型号',
  `memory` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '设备内存信息',
  `disk_space` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '设备硬盘空间',
  `disk_type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '硬盘类型SSD, STAT',
  `remark` varchar(155) COLLATE utf8_bin DEFAULT '' COMMENT '备注',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_host_id` (`host_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `host_pool_extend`
--

LOCK TABLES `host_pool_extend` WRITE;
/*!40000 ALTER TABLE `host_pool_extend` DISABLE KEYS */;
INSERT INTO `host_pool_extend` VALUES (1,'81804888-3027-11e8-9b98-fa163ea5419d','sbtest','192.168.0.92','','114.67.76.75','',4,'Intel Core Processor','16G','100G',0,'','2018-03-25 12:30:02','2018-03-25 13:28:57'),(2,'053c7088-310a-11e8-84ee-ac853dafc5c4','sbtest','192.168.1.1','','','',2,'Intel Core Processor','4G','10G',0,'','2018-03-26 15:30:05','2018-03-26 15:30:05');
/*!40000 ALTER TABLE `host_pool_extend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instance_pool`
--

DROP TABLE IF EXISTS `instance_pool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `instance_pool` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `host_id` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '主机唯一ID，自动生成',
  `instance_id` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '实例唯一ID，自动生成',
  `project_id` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '项目id',
  `instance_name` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '未命名' COMMENT '实例名称-用户自定义',
  `description` varchar(155) COLLATE utf8_bin NOT NULL DEFAULT '未标注' COMMENT '实例描述-用户自定义',
  `status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '主机运行状态，unknown;running;shutdown',
  `port` smallint(5) NOT NULL DEFAULT '3306' COMMENT '实例端口',
  `privateip` varchar(25) COLLATE utf8_bin NOT NULL COMMENT '私网地址',
  `type` varchar(25) COLLATE utf8_bin NOT NULL DEFAULT 'MySQL' COMMENT '服务类型，比如MySQL,Oracle...',
  `remark` varchar(255) COLLATE utf8_bin DEFAULT '' COMMENT '备注',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_host_id` (`host_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instance_pool`
--

LOCK TABLES `instance_pool` WRITE;
/*!40000 ALTER TABLE `instance_pool` DISABLE KEYS */;
INSERT INTO `instance_pool` VALUES (1,'81804888-3027-11e8-9b98-fa163ea5419d','0ce26d42-3029-11e8-9f0b-fa163ea5419d','01','未命名','未标注',0,3306,'192.168.0.92','mysql','','2018-03-25 12:43:10','2018-03-25 12:43:10');
/*!40000 ALTER TABLE `instance_pool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '项目id',
  `project_name` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '项目名称',
  `project_description` varchar(150) COLLATE utf8_bin NOT NULL DEFAULT '' COMMENT '项目描述',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_pid` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES (1,'01','hcloud','hcloud web端的数据库','2018-03-25 13:13:37','2018-03-25 13:13:37');
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-01 23:40:22
