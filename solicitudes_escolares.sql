-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.4.3 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.8.0.6908
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para solicitudes_escolares
CREATE DATABASE IF NOT EXISTS `solicitudes_escolares` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `solicitudes_escolares`;

-- Volcando estructura para tabla solicitudes_escolares.administradores
CREATE TABLE IF NOT EXISTS `administradores` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `cedula` varchar(20) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `usuario` varchar(100) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('superadmin','secretaria','docente') NOT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `usuario` (`usuario`),
  UNIQUE KEY `cedula` (`cedula`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.administradores: ~5 rows (aproximadamente)
INSERT INTO `administradores` (`id_admin`, `nombre`, `apellido`, `cedula`, `telefono`, `correo`, `usuario`, `contraseña`, `rol`) VALUES
	(1, 'Damian', 'Rivadeneira', '1723200653', '0984342426', 'damianrivadeneira58@gmail.com', 'Admin1', '123456', 'superadmin'),
	(2, 'Franklin', 'Ureña', '1754988657', '093748927', 'Franklinurena123@gmail.com', 'Secretaria1', '123456', 'secretaria'),
	(3, 'Juan', 'Mendoza', '1764100893', '0987691308', 'Juanmendo432@gmail.com', 'Secretaria2', '123456', 'secretaria'),
	(4, 'Alex ', 'Jacome', '17355368496', '0987562309', 'Alexjac566@gmail.com', 'Docente1', '123456', 'docente'),
	(5, 'Isaac', 'Vasquez', '17234007584', '0986234872', 'guatiazam858@gmail.com', 'Docente2', '123456', 'docente');

-- Volcando estructura para tabla solicitudes_escolares.auth_group
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.auth_group: ~0 rows (aproximadamente)

-- Volcando estructura para tabla solicitudes_escolares.auth_group_permissions
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.auth_group_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla solicitudes_escolares.auth_permission
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.auth_permission: ~24 rows (aproximadamente)
INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
	(1, 'Can add log entry', 1, 'add_logentry'),
	(2, 'Can change log entry', 1, 'change_logentry'),
	(3, 'Can delete log entry', 1, 'delete_logentry'),
	(4, 'Can view log entry', 1, 'view_logentry'),
	(5, 'Can add permission', 3, 'add_permission'),
	(6, 'Can change permission', 3, 'change_permission'),
	(7, 'Can delete permission', 3, 'delete_permission'),
	(8, 'Can view permission', 3, 'view_permission'),
	(9, 'Can add group', 2, 'add_group'),
	(10, 'Can change group', 2, 'change_group'),
	(11, 'Can delete group', 2, 'delete_group'),
	(12, 'Can view group', 2, 'view_group'),
	(13, 'Can add user', 4, 'add_user'),
	(14, 'Can change user', 4, 'change_user'),
	(15, 'Can delete user', 4, 'delete_user'),
	(16, 'Can view user', 4, 'view_user'),
	(17, 'Can add content type', 5, 'add_contenttype'),
	(18, 'Can change content type', 5, 'change_contenttype'),
	(19, 'Can delete content type', 5, 'delete_contenttype'),
	(20, 'Can view content type', 5, 'view_contenttype'),
	(21, 'Can add session', 6, 'add_session'),
	(22, 'Can change session', 6, 'change_session'),
	(23, 'Can delete session', 6, 'delete_session'),
	(24, 'Can view session', 6, 'view_session');

-- Volcando estructura para tabla solicitudes_escolares.auth_user
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.auth_user: ~0 rows (aproximadamente)

-- Volcando estructura para tabla solicitudes_escolares.auth_user_groups
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.auth_user_groups: ~0 rows (aproximadamente)

-- Volcando estructura para tabla solicitudes_escolares.auth_user_user_permissions
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.auth_user_user_permissions: ~0 rows (aproximadamente)

-- Volcando estructura para tabla solicitudes_escolares.django_admin_log
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.django_admin_log: ~0 rows (aproximadamente)

-- Volcando estructura para tabla solicitudes_escolares.django_content_type
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.django_content_type: ~6 rows (aproximadamente)
INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
	(1, 'admin', 'logentry'),
	(2, 'auth', 'group'),
	(3, 'auth', 'permission'),
	(4, 'auth', 'user'),
	(5, 'contenttypes', 'contenttype'),
	(6, 'sessions', 'session');

-- Volcando estructura para tabla solicitudes_escolares.django_migrations
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.django_migrations: ~18 rows (aproximadamente)
INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
	(1, 'contenttypes', '0001_initial', '2026-06-09 02:49:36.986549'),
	(2, 'auth', '0001_initial', '2026-06-09 02:49:37.390544'),
	(3, 'admin', '0001_initial', '2026-06-09 02:49:37.545911'),
	(4, 'admin', '0002_logentry_remove_auto_add', '2026-06-09 02:49:37.553719'),
	(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-06-09 02:49:37.558502'),
	(6, 'contenttypes', '0002_remove_content_type_name', '2026-06-09 02:49:37.617594'),
	(7, 'auth', '0002_alter_permission_name_max_length', '2026-06-09 02:49:37.666543'),
	(8, 'auth', '0003_alter_user_email_max_length', '2026-06-09 02:49:37.683348'),
	(9, 'auth', '0004_alter_user_username_opts', '2026-06-09 02:49:37.689977'),
	(10, 'auth', '0005_alter_user_last_login_null', '2026-06-09 02:49:37.737143'),
	(11, 'auth', '0006_require_contenttypes_0002', '2026-06-09 02:49:37.738935'),
	(12, 'auth', '0007_alter_validators_add_error_messages', '2026-06-09 02:49:37.744230'),
	(13, 'auth', '0008_alter_user_username_max_length', '2026-06-09 02:49:37.799943'),
	(14, 'auth', '0009_alter_user_last_name_max_length', '2026-06-09 02:49:37.850347'),
	(15, 'auth', '0010_alter_group_name_max_length', '2026-06-09 02:49:37.864465'),
	(16, 'auth', '0011_update_proxy_permissions', '2026-06-09 02:49:37.870433'),
	(17, 'auth', '0012_alter_user_first_name_max_length', '2026-06-09 02:49:37.916996'),
	(18, 'sessions', '0001_initial', '2026-06-09 02:49:37.942960');

-- Volcando estructura para tabla solicitudes_escolares.django_session
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.django_session: ~1 rows (aproximadamente)
INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
	('8fqjfs53enzi45r2ss07wxor94zzsn61', 'eyJhZG1pbl9pZCI6MiwiYWRtaW5fcm9sZSI6InNlY3JldGFyaWEifQ:1wYwvn:xuDmbYBWePKpC4yyfti3Vzadj7Dr-LfBeu1GHapsQhI', '2026-06-29 02:20:07.054113');

-- Volcando estructura para tabla solicitudes_escolares.solicitudes
CREATE TABLE IF NOT EXISTS `solicitudes` (
  `id_solicitud` int NOT NULL AUTO_INCREMENT,
  `codigo` varchar(20) DEFAULT NULL,
  `nombre_solicitante` varchar(150) NOT NULL,
  `cedula_solicitante` varchar(20) DEFAULT NULL,
  `telefono_solicitante` varchar(20) DEFAULT NULL,
  `nombre_estudiante` varchar(150) NOT NULL,
  `seccion` enum('Guamani','Cojimies') DEFAULT NULL,
  `jornada` enum('Matutina','Semipresencial') DEFAULT NULL,
  `nivel` enum('Maternal','Inicial','EGB','Bachillerato Técnico','Básico Intensivo','Bachillerato Intensivo','Bachillerato Técnico Intensivo') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `descripcion` text,
  `anexos` text,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('pendiente','recibido','en_proceso','resuelto','rechazado','asignada') NOT NULL DEFAULT 'pendiente',
  `grado` enum('Maternal','Inicial','1ro','2do','3ro','4to','5to','6to','7mo','8vo','9no','10mo','1ero Bach','2do Bach','3ro Bach') NOT NULL,
  `paralelo` enum('A','B','C','D','E','F') DEFAULT NULL,
  `tecnica` varchar(100) DEFAULT NULL,
  `paralelo_tecnico` varchar(50) DEFAULT NULL,
  `id_responsable` int DEFAULT NULL,
  `respuesta` text,
  `fecha_actualizacion` timestamp NULL DEFAULT NULL,
  `correo_solicitante` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id_solicitud`),
  KEY `fk_responsable` (`id_responsable`),
  CONSTRAINT `fk_responsable` FOREIGN KEY (`id_responsable`) REFERENCES `administradores` (`id_admin`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla solicitudes_escolares.solicitudes: ~3 rows (aproximadamente)
INSERT INTO `solicitudes` (`id_solicitud`, `codigo`, `nombre_solicitante`, `cedula_solicitante`, `telefono_solicitante`, `nombre_estudiante`, `seccion`, `jornada`, `nivel`, `descripcion`, `anexos`, `fecha_creacion`, `estado`, `grado`, `paralelo`, `tecnica`, `paralelo_tecnico`, `id_responsable`, `respuesta`, `fecha_actualizacion`, `correo_solicitante`) VALUES
	(1, 'SOL-0001', 'Maria Lopez', '1723456789', '0988888888', 'Juan Lopez', 'Guamani', 'Semipresencial', 'Bachillerato Técnico Intensivo', 'Solicito certificado', 'Captura_de_pantalla_2026-05-23_123420.png', '2026-04-23 20:53:28', 'resuelto', '3ro Bach', 'B', 'Informática', 'B', 4, 'Porfavor venir al cole', '2026-06-12 06:52:44', 'damianrivadeneira858@gmail.com'),
	(2, 'SOL-0003', 'Erika Dayana', '1723200753', '0984342426', 'Damian rivadeneira', 'Guamani', 'Matutina', 'Bachillerato Técnico', 'Devolución de dinero', 'captura_1.png', '2026-05-15 13:09:32', 'en_proceso', '3ro Bach', 'B', 'Informática', 'A', 4, 'Solicitud enviada el Docente Alex Jacome ', '2026-06-12 05:46:27', 'damianrivadeneira858@gmail.com'),
	(3, 'SOL-0004', 'Martina Ureña', '1723200757', '0984342426', 'Gabriel Ureña ', 'Guamani', 'Matutina', 'Bachillerato Intensivo', 'Reporte de notas de los ultimos 5 años ', 'Captura_de_pantalla_2026-05-23_123420.png', '2026-05-29 22:34:31', 'pendiente', '10mo', 'D', NULL, NULL, 4, 'solicityd ini', '2026-06-12 00:17:25', 'damianrivadeneira858@gmail.com');

-- Volcando estructura para disparador solicitudes_escolares.generar_codigo_solicitud
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `generar_codigo_solicitud` BEFORE INSERT ON `solicitudes` FOR EACH ROW BEGIN
    DECLARE nuevo_codigo VARCHAR(20);

    SET nuevo_codigo = CONCAT('SOL-', LPAD((SELECT IFNULL(MAX(id_solicitud)+1,1) FROM solicitudes), 4, '0'));

    SET NEW.codigo = nuevo_codigo;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
