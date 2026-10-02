-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: sql_chatbot
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `registration_date` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Aarav Sharma','aarav@gmail.com','Pune',25,'Male','2025-01-15'),(2,'Priya Patil','priya@gmail.com','Mumbai',29,'Female','2025-01-20'),(3,'Rohan Deshmukh','rohan@gmail.com','Nashik',32,'Male','2025-02-05'),(4,'Sneha Kulkarni','sneha@gmail.com','Pune',27,'Female','2025-02-18'),(5,'Aditya Joshi','aditya@gmail.com','Nagpur',24,'Male','2025-03-02'),(6,'Neha Shah','neha@gmail.com','Mumbai',31,'Female','2025-03-15'),(7,'Rahul Jadhav','rahul@gmail.com','Pune',35,'Male','2025-03-22'),(8,'Ananya Mehta','ananya@gmail.com','Delhi',26,'Female','2025-04-01'),(9,'Vikram Singh','vikram@gmail.com','Bangalore',30,'Male','2025-04-12'),(10,'Isha More','isha@gmail.com','Nashik',23,'Female','2025-04-25'),(11,'Kunal Pawar','kunal@gmail.com','Pune',28,'Male','2025-05-05'),(12,'Pooja Chavan','pooja@gmail.com','Mumbai',34,'Female','2025-05-17'),(13,'Siddharth Rao','siddharth@gmail.com','Hyderabad',29,'Male','2025-06-03'),(14,'Meera Joshi','meera@gmail.com','Pune',25,'Female','2025-06-15'),(15,'Akash Gupta','akash@gmail.com','Delhi',33,'Male','2025-06-28');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `customer_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,1,1,'2025-07-01','Delivered','UPI'),(2,1,2,2,'2025-07-01','Delivered','UPI'),(3,2,4,1,'2025-07-03','Delivered','Credit Card'),(4,2,5,2,'2025-07-10','Delivered','Credit Card'),(5,3,7,1,'2025-07-05','Delivered','UPI'),(6,3,8,1,'2025-07-05','Delivered','Cash'),(7,4,3,1,'2025-07-08','Delivered','UPI'),(8,4,6,1,'2025-07-15','Delivered','Debit Card'),(9,5,9,1,'2025-07-12','Delivered','Credit Card'),(10,5,11,3,'2025-07-20','Delivered','UPI'),(11,6,4,1,'2025-07-18','Delivered','UPI'),(12,6,12,1,'2025-07-25','Cancelled','UPI'),(13,7,1,1,'2025-08-01','Delivered','Credit Card'),(14,7,3,2,'2025-08-03','Delivered','UPI'),(15,8,6,1,'2025-08-05','Delivered','Debit Card'),(16,8,7,2,'2025-08-10','Delivered','UPI'),(17,9,4,1,'2025-08-12','Delivered','Credit Card'),(18,9,5,1,'2025-08-15','Delivered','UPI'),(19,10,8,2,'2025-08-18','Delivered','Cash'),(20,10,11,2,'2025-08-20','Delivered','UPI'),(21,11,2,3,'2025-08-22','Delivered','UPI'),(22,11,5,1,'2025-08-25','Delivered','Credit Card'),(23,12,10,1,'2025-08-27','Delivered','Debit Card'),(24,12,7,1,'2025-08-29','Delivered','UPI'),(25,13,1,1,'2025-09-01','Delivered','Credit Card'),(26,13,6,1,'2025-09-03','Delivered','UPI'),(27,14,3,2,'2025-09-05','Delivered','UPI'),(28,14,8,1,'2025-09-07','Delivered','Credit Card'),(29,15,4,1,'2025-09-10','Delivered','UPI'),(30,15,9,1,'2025-09-12','Delivered','Credit Card'),(31,1,6,1,'2025-09-15','Delivered','UPI'),(32,2,1,1,'2025-09-16','Delivered','Credit Card'),(33,3,5,2,'2025-09-18','Delivered','UPI'),(34,4,11,4,'2025-09-20','Delivered','Cash'),(35,5,4,1,'2025-09-22','Delivered','UPI'),(36,6,8,1,'2025-09-23','Delivered','Credit Card'),(37,7,7,1,'2025-09-24','Delivered','UPI'),(38,8,2,2,'2025-09-25','Delivered','Debit Card'),(39,9,10,1,'2025-09-26','Delivered','UPI'),(40,10,12,1,'2025-09-27','Delivered','Credit Card'),(41,1,1,1,'2025-07-01','Delivered','UPI'),(42,1,2,2,'2025-07-01','Delivered','UPI'),(43,2,4,1,'2025-07-03','Delivered','Credit Card'),(44,2,5,2,'2025-07-10','Delivered','Credit Card'),(45,3,7,1,'2025-07-05','Delivered','UPI'),(46,3,8,1,'2025-07-05','Delivered','Cash'),(47,4,3,1,'2025-07-08','Delivered','UPI'),(48,4,6,1,'2025-07-15','Delivered','Debit Card'),(49,5,9,1,'2025-07-12','Delivered','Credit Card'),(50,5,11,3,'2025-07-20','Delivered','UPI'),(51,6,4,1,'2025-07-18','Delivered','UPI'),(52,6,12,1,'2025-07-25','Cancelled','UPI'),(53,7,1,1,'2025-08-01','Delivered','Credit Card'),(54,7,3,2,'2025-08-03','Delivered','UPI'),(55,8,6,1,'2025-08-05','Delivered','Debit Card'),(56,8,7,2,'2025-08-10','Delivered','UPI'),(57,9,4,1,'2025-08-12','Delivered','Credit Card'),(58,9,5,1,'2025-08-15','Delivered','UPI'),(59,10,8,2,'2025-08-18','Delivered','Cash'),(60,10,11,2,'2025-08-20','Delivered','UPI'),(61,11,2,3,'2025-08-22','Delivered','UPI'),(62,11,5,1,'2025-08-25','Delivered','Credit Card'),(63,12,10,1,'2025-08-27','Delivered','Debit Card'),(64,12,7,1,'2025-08-29','Delivered','UPI'),(65,13,1,1,'2025-09-01','Delivered','Credit Card'),(66,13,6,1,'2025-09-03','Delivered','UPI'),(67,14,3,2,'2025-09-05','Delivered','UPI'),(68,14,8,1,'2025-09-07','Delivered','Credit Card'),(69,15,4,1,'2025-09-10','Delivered','UPI'),(70,15,9,1,'2025-09-12','Delivered','Credit Card'),(71,1,6,1,'2025-09-15','Delivered','UPI'),(72,2,1,1,'2025-09-16','Delivered','Credit Card'),(73,3,5,2,'2025-09-18','Delivered','UPI'),(74,4,11,4,'2025-09-20','Delivered','Cash'),(75,5,4,1,'2025-09-22','Delivered','UPI'),(76,6,8,1,'2025-09-23','Delivered','Credit Card'),(77,7,7,1,'2025-09-24','Delivered','UPI'),(78,8,2,2,'2025-09-25','Delivered','Debit Card'),(79,9,10,1,'2025-09-26','Delivered','UPI'),(80,10,12,1,'2025-09-27','Delivered','Credit Card'),(81,1,1,1,'2025-07-01','Delivered','UPI'),(82,1,2,2,'2025-07-01','Delivered','UPI'),(83,2,4,1,'2025-07-03','Delivered','Credit Card'),(84,2,5,2,'2025-07-10','Delivered','Credit Card'),(85,3,7,1,'2025-07-05','Delivered','UPI'),(86,3,8,1,'2025-07-05','Delivered','Cash'),(87,4,3,1,'2025-07-08','Delivered','UPI'),(88,4,6,1,'2025-07-15','Delivered','Debit Card'),(89,5,9,1,'2025-07-12','Delivered','Credit Card'),(90,5,11,3,'2025-07-20','Delivered','UPI'),(91,6,4,1,'2025-07-18','Delivered','UPI'),(92,6,12,1,'2025-07-25','Cancelled','UPI'),(93,7,1,1,'2025-08-01','Delivered','Credit Card'),(94,7,3,2,'2025-08-03','Delivered','UPI'),(95,8,6,1,'2025-08-05','Delivered','Debit Card'),(96,8,7,2,'2025-08-10','Delivered','UPI'),(97,9,4,1,'2025-08-12','Delivered','Credit Card'),(98,9,5,1,'2025-08-15','Delivered','UPI'),(99,10,8,2,'2025-08-18','Delivered','Cash'),(100,10,11,2,'2025-08-20','Delivered','UPI'),(101,11,2,3,'2025-08-22','Delivered','UPI'),(102,11,5,1,'2025-08-25','Delivered','Credit Card'),(103,12,10,1,'2025-08-27','Delivered','Debit Card'),(104,12,7,1,'2025-08-29','Delivered','UPI'),(105,13,1,1,'2025-09-01','Delivered','Credit Card'),(106,13,6,1,'2025-09-03','Delivered','UPI'),(107,14,3,2,'2025-09-05','Delivered','UPI'),(108,14,8,1,'2025-09-07','Delivered','Credit Card'),(109,15,4,1,'2025-09-10','Delivered','UPI'),(110,15,9,1,'2025-09-12','Delivered','Credit Card'),(111,1,6,1,'2025-09-15','Delivered','UPI'),(112,2,1,1,'2025-09-16','Delivered','Credit Card'),(113,3,5,2,'2025-09-18','Delivered','UPI'),(114,4,11,4,'2025-09-20','Delivered','Cash'),(115,5,4,1,'2025-09-22','Delivered','UPI'),(116,6,8,1,'2025-09-23','Delivered','Credit Card'),(117,7,7,1,'2025-09-24','Delivered','UPI'),(118,8,2,2,'2025-09-25','Delivered','Debit Card'),(119,9,10,1,'2025-09-26','Delivered','UPI'),(120,10,12,1,'2025-09-27','Delivered','Credit Card'),(121,1,1,1,'2025-07-01','Delivered','UPI'),(122,1,2,2,'2025-07-01','Delivered','UPI'),(123,2,4,1,'2025-07-03','Delivered','Credit Card'),(124,2,5,2,'2025-07-10','Delivered','Credit Card'),(125,3,7,1,'2025-07-05','Delivered','UPI'),(126,3,8,1,'2025-07-05','Delivered','Cash'),(127,4,3,1,'2025-07-08','Delivered','UPI'),(128,4,6,1,'2025-07-15','Delivered','Debit Card'),(129,5,9,1,'2025-07-12','Delivered','Credit Card'),(130,5,11,3,'2025-07-20','Delivered','UPI'),(131,6,4,1,'2025-07-18','Delivered','UPI'),(132,6,12,1,'2025-07-25','Cancelled','UPI'),(133,7,1,1,'2025-08-01','Delivered','Credit Card'),(134,7,3,2,'2025-08-03','Delivered','UPI'),(135,8,6,1,'2025-08-05','Delivered','Debit Card'),(136,8,7,2,'2025-08-10','Delivered','UPI'),(137,9,4,1,'2025-08-12','Delivered','Credit Card'),(138,9,5,1,'2025-08-15','Delivered','UPI'),(139,10,8,2,'2025-08-18','Delivered','Cash'),(140,10,11,2,'2025-08-20','Delivered','UPI'),(141,11,2,3,'2025-08-22','Delivered','UPI'),(142,11,5,1,'2025-08-25','Delivered','Credit Card'),(143,12,10,1,'2025-08-27','Delivered','Debit Card'),(144,12,7,1,'2025-08-29','Delivered','UPI'),(145,13,1,1,'2025-09-01','Delivered','Credit Card'),(146,13,6,1,'2025-09-03','Delivered','UPI'),(147,14,3,2,'2025-09-05','Delivered','UPI'),(148,14,8,1,'2025-09-07','Delivered','Credit Card'),(149,15,4,1,'2025-09-10','Delivered','UPI'),(150,15,9,1,'2025-09-12','Delivered','Credit Card'),(151,1,6,1,'2025-09-15','Delivered','UPI'),(152,2,1,1,'2025-09-16','Delivered','Credit Card'),(153,3,5,2,'2025-09-18','Delivered','UPI'),(154,4,11,4,'2025-09-20','Delivered','Cash'),(155,5,4,1,'2025-09-22','Delivered','UPI'),(156,6,8,1,'2025-09-23','Delivered','Credit Card'),(157,7,7,1,'2025-09-24','Delivered','UPI'),(158,8,2,2,'2025-09-25','Delivered','Debit Card'),(159,9,10,1,'2025-09-26','Delivered','UPI'),(160,10,12,1,'2025-09-27','Delivered','Credit Card');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(150) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Laptop Pro 14','Electronics',75000.00,25),(2,'Wireless Mouse','Electronics',1200.00,100),(3,'Mechanical Keyboard','Electronics',3500.00,60),(4,'Smartphone X','Electronics',45000.00,30),(5,'Bluetooth Headphones','Electronics',2500.00,80),(6,'Smart Watch','Wearables',6000.00,45),(7,'Running Shoes','Fashion',3200.00,70),(8,'Backpack','Fashion',1800.00,90),(9,'Office Chair','Furniture',8500.00,20),(10,'Study Table','Furniture',6500.00,15),(11,'Water Bottle','Lifestyle',700.00,150),(12,'Fitness Band','Wearables',2200.00,55);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-10-02 10:30:33
