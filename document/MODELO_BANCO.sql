-- --------------------------------------------------------
-- Host:                         192.185.217.47
-- Server version:               5.7.23-23 - Percona Server (GPL), Release 23, Revision 500fcf5
-- Server OS:                    Linux
-- HeidiSQL Version:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table bsconsul_fiap.APLICACAO_NUTRIENTE
CREATE TABLE IF NOT EXISTS `APLICACAO_NUTRIENTE` (
  `cd_aplicacao_nutriente` bigint(20) NOT NULL,
  `qtd` double NOT NULL,
  `cd_aplicacao` bigint(20) NOT NULL,
  `cd_nutriente` bigint(20) NOT NULL,
  PRIMARY KEY (`cd_aplicacao_nutriente`),
  KEY `cd_aplicacao` (`cd_aplicacao`),
  KEY `cd_nutriente` (`cd_nutriente`),
  CONSTRAINT `APLICACAO_NUTRIENTE_ibfk_1` FOREIGN KEY (`cd_aplicacao`) REFERENCES `APLICACAO_RECURSO` (`cd_aplicacao`),
  CONSTRAINT `APLICACAO_NUTRIENTE_ibfk_2` FOREIGN KEY (`cd_nutriente`) REFERENCES `NUTRIENTE` (`cd_nutriente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.APLICACAO_RECURSO
CREATE TABLE IF NOT EXISTS `APLICACAO_RECURSO` (
  `cd_aplicacao` bigint(20) NOT NULL,
  `cd_cultura` bigint(20) NOT NULL,
  `data_hora` datetime NOT NULL,
  `qtd_agua` double DEFAULT NULL,
  PRIMARY KEY (`cd_aplicacao`),
  KEY `cd_cultura` (`cd_cultura`),
  CONSTRAINT `APLICACAO_RECURSO_ibfk_1` FOREIGN KEY (`cd_cultura`) REFERENCES `CULTURA` (`cd_cultura`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.CULTURA
CREATE TABLE IF NOT EXISTS `CULTURA` (
  `cd_cultura` bigint(20) NOT NULL,
  `cd_produtor` bigint(20) NOT NULL,
  `nome` varchar(55) COLLATE utf8_unicode_ci NOT NULL,
  `tipo` varchar(55) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`cd_cultura`),
  KEY `cd_produtor` (`cd_produtor`),
  CONSTRAINT `CULTURA_ibfk_1` FOREIGN KEY (`cd_produtor`) REFERENCES `PRODUTOR` (`cd_produtor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.DECISAO_IRRIGACAO
CREATE TABLE IF NOT EXISTS `DECISAO_IRRIGACAO` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  `pode_irrigar` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.LEITURA_SENSOR
CREATE TABLE IF NOT EXISTS `LEITURA_SENSOR` (
  `cd_leitura` bigint(20) NOT NULL AUTO_INCREMENT,
  `cd_sensor_instalado` bigint(20) NOT NULL,
  `data_hora` datetime NOT NULL,
  `valor_umidade` double DEFAULT NULL,
  `valor_ph` double DEFAULT NULL,
  `valor_fosforo` double DEFAULT NULL,
  `valor_potassio` double DEFAULT NULL,
  PRIMARY KEY (`cd_leitura`),
  KEY `cd_sensor_instalado` (`cd_sensor_instalado`),
  CONSTRAINT `LEITURA_SENSOR_ibfk_1` FOREIGN KEY (`cd_sensor_instalado`) REFERENCES `SENSOR_INSTALADO` (`cd_sensor_instalado`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.NUTRIENTE
CREATE TABLE IF NOT EXISTS `NUTRIENTE` (
  `cd_nutriente` bigint(20) NOT NULL,
  `nome` varchar(55) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`cd_nutriente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.PRODUTOR
CREATE TABLE IF NOT EXISTS `PRODUTOR` (
  `cd_produtor` bigint(20) NOT NULL,
  `nome` varchar(55) COLLATE utf8_unicode_ci NOT NULL,
  `fazenda` varchar(55) COLLATE utf8_unicode_ci NOT NULL,
  `localizacao` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`cd_produtor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.SENSOR
CREATE TABLE IF NOT EXISTS `SENSOR` (
  `cd_sensor` bigint(20) NOT NULL,
  `tipo` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `nome` varchar(55) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`cd_sensor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table bsconsul_fiap.SENSOR_INSTALADO
CREATE TABLE IF NOT EXISTS `SENSOR_INSTALADO` (
  `cd_sensor_instalado` bigint(20) NOT NULL,
  `cd_cultura` bigint(20) NOT NULL,
  `cd_sensor` bigint(20) NOT NULL,
  `data_instalacao` datetime NOT NULL,
  PRIMARY KEY (`cd_sensor_instalado`),
  KEY `cd_cultura` (`cd_cultura`),
  KEY `cd_sensor` (`cd_sensor`),
  CONSTRAINT `SENSOR_INSTALADO_ibfk_1` FOREIGN KEY (`cd_cultura`) REFERENCES `CULTURA` (`cd_cultura`),
  CONSTRAINT `SENSOR_INSTALADO_ibfk_2` FOREIGN KEY (`cd_sensor`) REFERENCES `SENSOR` (`cd_sensor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
