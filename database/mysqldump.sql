-- MySQL dump 10.13  Distrib 8.1.0, for Linux (aarch64)
--
-- Host: localhost    Database: uni
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
-- Table structure for table `tblAcademic`
--

DROP TABLE IF EXISTS `tblAcademic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblAcademic` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `zID` int DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `academicType` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `zID` (`zID`),
  KEY `school` (`school`),
  CONSTRAINT `tblAcademic_ibfk_1` FOREIGN KEY (`zID`) REFERENCES `tblUser` (`zID`),
  CONSTRAINT `tblAcademic_ibfk_2` FOREIGN KEY (`school`) REFERENCES `tblSchool` (`schoolName`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblAcademic`
--

LOCK TABLES `tblAcademic` WRITE;
/*!40000 ALTER TABLE `tblAcademic` DISABLE KEYS */;
INSERT INTO `tblAcademic` VALUES (1,5319978,'Engineering','banana');
/*!40000 ALTER TABLE `tblAcademic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblMajor`
--

DROP TABLE IF EXISTS `tblMajor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblMajor` (
  `ID` varchar(6) NOT NULL,
  `majorName` varchar(255) DEFAULT NULL,
  `program` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `program` (`program`),
  CONSTRAINT `tblMajor_ibfk_1` FOREIGN KEY (`program`) REFERENCES `tblProgram` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblMajor`
--

LOCK TABLES `tblMajor` WRITE;
/*!40000 ALTER TABLE `tblMajor` DISABLE KEYS */;
INSERT INTO `tblMajor` VALUES ('COMPA1','Default',3778),('COMPD1','Database Systems',3778),('COMPE1','eCommerce Systems',3778),('COMPI1','Artificial Intelligence',3778),('COMPJ1','Programming Langauges',3778),('COMPN1','Computer Networks',3778),('COMPS1','Embedded Systems',3778),('COMPY1','Security Engineering',3778);
/*!40000 ALTER TABLE `tblMajor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblProgram`
--

DROP TABLE IF EXISTS `tblProgram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblProgram` (
  `ID` int NOT NULL,
  `programName` varchar(255) DEFAULT NULL,
  `managingSchool` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `managingSchool` (`managingSchool`),
  CONSTRAINT `tblProgram_ibfk_1` FOREIGN KEY (`managingSchool`) REFERENCES `tblSchool` (`schoolName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblProgram`
--

LOCK TABLES `tblProgram` WRITE;
/*!40000 ALTER TABLE `tblProgram` DISABLE KEYS */;
INSERT INTO `tblProgram` VALUES (3132,'Materials Science and Engineering (Honours) / Engineering Science','Arts, Design & Architecture'),(3778,'Computer Science','Engineering');
/*!40000 ALTER TABLE `tblProgram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblSchool`
--

DROP TABLE IF EXISTS `tblSchool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblSchool` (
  `schoolName` varchar(255) NOT NULL,
  PRIMARY KEY (`schoolName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblSchool`
--

LOCK TABLES `tblSchool` WRITE;
/*!40000 ALTER TABLE `tblSchool` DISABLE KEYS */;
INSERT INTO `tblSchool` VALUES ('Arts, Design & Architecture'),('Business School'),('Engineering'),('Law and Justice'),('Medicine and Health'),('Science');
/*!40000 ALTER TABLE `tblSchool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblStudent`
--

DROP TABLE IF EXISTS `tblStudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblStudent` (
  `zID` int NOT NULL,
  `transcript` varchar(255) DEFAULT NULL,
  `program` int DEFAULT NULL,
  `major` varchar(7) DEFAULT NULL,
  PRIMARY KEY (`zID`),
  KEY `program` (`program`),
  KEY `major` (`major`),
  CONSTRAINT `tblStudent_ibfk_1` FOREIGN KEY (`program`) REFERENCES `tblProgram` (`ID`),
  CONSTRAINT `tblStudent_ibfk_2` FOREIGN KEY (`major`) REFERENCES `tblMajor` (`ID`),
  CONSTRAINT `tblStudent_ibfk_3` FOREIGN KEY (`zID`) REFERENCES `tblUser` (`zID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblStudent`
--

LOCK TABLES `tblStudent` WRITE;
/*!40000 ALTER TABLE `tblStudent` DISABLE KEYS */;
/*!40000 ALTER TABLE `tblStudent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblUser`
--

DROP TABLE IF EXISTS `tblUser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblUser` (
  `firstname` varchar(100) DEFAULT NULL,
  `lastname` varchar(100) DEFAULT NULL,
  `zID` int NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `enPassword` varchar(255) DEFAULT NULL,
  `contactNumber` bigint DEFAULT NULL,
  `userRole` int DEFAULT NULL,
  PRIMARY KEY (`zID`),
  KEY `userRole` (`userRole`),
  CONSTRAINT `tblUser_ibfk_1` FOREIGN KEY (`userRole`) REFERENCES `tblUserRole` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblUser`
--

LOCK TABLES `tblUser` WRITE;
/*!40000 ALTER TABLE `tblUser` DISABLE KEYS */;
INSERT INTO `tblUser` VALUES ('C','D',5319978,'banana@gmail.com','2000-07-13','banana',61123456789,1);
/*!40000 ALTER TABLE `tblUser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tblUserRole`
--

DROP TABLE IF EXISTS `tblUserRole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tblUserRole` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `userRoleName` varchar(128) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `userRoleName` (`userRoleName`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tblUserRole`
--

LOCK TABLES `tblUserRole` WRITE;
/*!40000 ALTER TABLE `tblUserRole` DISABLE KEYS */;
INSERT INTO `tblUserRole` VALUES (1,'Admin');
/*!40000 ALTER TABLE `tblUserRole` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-10-05  8:55:28
