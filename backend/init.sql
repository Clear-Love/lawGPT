-- MySQL dump 10.13  Distrib 8.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: lawDB
-- ------------------------------------------------------
-- Server version	8.1.0

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
-- Table structure for table `content`
--

DROP TABLE IF EXISTS `content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `content` (
  `id` varchar(255) NOT NULL COMMENT 'id',
  `conversation_id` varchar(255) NOT NULL COMMENT '所属对话id',
  `content` text NOT NULL COMMENT '内容',
  `create_time` timestamp NOT NULL DEFAULT (now()) COMMENT '生成时间',
  `role` varchar(16) NOT NULL COMMENT '角色',
  `parent` varchar(255) DEFAULT NULL COMMENT '父结点',
  PRIMARY KEY (`id`),
  KEY `content_conversation_id_fk` (`conversation_id`),
  KEY `content_content_id_fk` (`parent`),
  CONSTRAINT `content_conversation_id_fk` FOREIGN KEY (`conversation_id`) REFERENCES `conversation` (`id`),
  CONSTRAINT `role_check` CHECK ((`role` in (_utf8mb4'system',_utf8mb4'user',_utf8mb4'assistant')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='对话上下文';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `content`
--

LOCK TABLES `content` WRITE;
/*!40000 ALTER TABLE `content` DISABLE KEYS */;
/*!40000 ALTER TABLE `content` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversation`
--

DROP TABLE IF EXISTS `conversation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversation` (
  `id` varchar(255) NOT NULL COMMENT '对话id',
  `user_id` int NOT NULL COMMENT '所属用户id',
  `title` varchar(255) NOT NULL COMMENT '标题',
  `create_time` datetime NOT NULL DEFAULT (now()) COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT (now()) COMMENT '更新时间',
  `curr_content` varchar(255) DEFAULT NULL COMMENT '当前对话结点',
  `type` varchar(16) NOT NULL COMMENT '对话类型',
  PRIMARY KEY (`id`),
  KEY `conversation_user_id_fk` (`user_id`),
  KEY `conversation_content_id_fk` (`curr_content`),
  CONSTRAINT `conversation_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='对话';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversation`
--

LOCK TABLES `conversation` WRITE;
/*!40000 ALTER TABLE `conversation` DISABLE KEYS */;
/*!40000 ALTER TABLE `conversation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `username` varchar(32) NOT NULL COMMENT '用户名',
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `create_time` datetime NOT NULL DEFAULT (now()) COMMENT '创建时间',
  `hashed_password` varchar(128) NOT NULL COMMENT '密码',
  `email` varchar(128) NOT NULL COMMENT '邮箱',
  `is_active` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否可以用',
  `is_superuser` tinyint(1) NOT NULL COMMENT '是否为超级用户',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `is_verified` tinyint(1) NOT NULL COMMENT '是否已验证',
  `last_active_time` datetime NOT NULL DEFAULT (now()) COMMENT '最后活跃时间',
  `nickname` varchar(32) DEFAULT NULL COMMENT '昵称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_pk` (`username`,`email`),
  UNIQUE KEY `user_pk2` (`username`,`email`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin',25,'2023-11-18 14:59:32','$2b$12$YDeTgtbIHO.yvRze/Qfwq.bFhLPATdTacLa42SEvxpYrvCAHsWGhS','123@123.com',1,0,'string',0,'2023-12-23 07:59:08','admin'),('lmio',26,'2023-12-01 10:30:04','$2b$12$dRSkG9hudiNZx0vtf4v6s.jvvct56LWu9KugcOAOkUhEtX5/3k8e.','2091319361@qq.com',1,0,'',0,'2023-12-01 14:31:47','lmio');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-23 18:20:32
