
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

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
TRUNCATE TABLE `users`;
INSERT INTO `users` (`id`, `name`, `age`, `nationality`, `date_of_birth`) VALUES (1,'U1',28,'IN','1997-03-10'),(2,'U2',17,'US','2008-07-22'),(3,'U3',35,'IN','1990-11-05'),(4,'U4',22,'UK','2003-01-15'),(5,'U5',16,'IN','2009-09-30');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
TRUNCATE TABLE `companies`;
INSERT INTO `companies` (`id`, `name`, `industry`, `country`, `bank_deposit`) VALUES (1,'C1','health','IN',50000.00),(2,'C2','health','US',500.00),(3,'C3','health','IN',50000.00),(4,'C4','health','UK',500.00),(5,'C5','health','US',50000.00);
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;

/*!40000 ALTER TABLE `rules` DISABLE KEYS */;
TRUNCATE TABLE `rules`;
INSERT INTO `rules` (`id`, `field_name`, `operator`, `value`, `name`) VALUES (1,'User.age','>=','21','Adult'),(2,'User.nationality','==','IN','Indian'),(3,'Contract.is_active','==','true','ActiveContract'),(4,'Company.bank_deposit','>=','50000.00','BankDeposit50k'),(5,'User.nationality','==','{{country}}','TemplateNationality'),(6,'User.age','>','{{age}}','TemplateAge'),(7,'Company.industry','==','{{industry}}','TemplateIndustry'),(8,'Company.bank_deposit','>=','{{deposit}}','TemplateDeposit'),(9,'__composite__','AND','1,2','IndianAdult'),(10,'__composite__','AND','1,3','AdultActive'),(11,'__composite__','AND','1,2,3','IndianAdultActive'),(12,'__composite__','OR','2,4','IndianOrDeposit'),(13,'__composite__','AND','11,12','FullCompliance'),(14,'__composite__','AND','5,6','TemplateDrivingAge');
/*!40000 ALTER TABLE `rules` ENABLE KEYS */;

/*!40000 ALTER TABLE `contracts` DISABLE KEYS */;
TRUNCATE TABLE `contracts`;
INSERT INTO `contracts` (`id`, `user_id`, `company_id`, `start_date`, `end_date`, `country`, `is_active`) VALUES (1,1,1,'2025-01-01 00:00:00','2027-01-01 00:00:00','IN',1),(2,2,1,'2025-06-01 00:00:00','2026-06-01 00:00:00','IN',1),(3,3,2,'2025-03-01 00:00:00','2027-03-01 00:00:00','US',1),(4,4,3,'2025-05-01 00:00:00','2026-05-01 00:00:00','UK',1),(5,1,2,'2023-01-01 00:00:00','2024-01-01 00:00:00','US',0),(6,5,3,'2023-06-01 00:00:00','2024-06-01 00:00:00','IN',0),(7,3,4,'2022-01-01 00:00:00','2023-01-01 00:00:00','UK',0);
/*!40000 ALTER TABLE `contracts` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

