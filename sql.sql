/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `war-game` /*!40100 DEFAULT CHARACTER SET armscii8 COLLATE armscii8_bin */;
USE `war-game`;

CREATE TABLE IF NOT EXISTS `temp_users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '고유 id',
  `email` varchar(320) COLLATE utf8mb4_bin NOT NULL COMMENT '이메일 최대값',
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '이름',
  `password` binary(60) NOT NULL COMMENT '비밀번호',
  `verify_code` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '인증코드',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '고유id',
  `email` varchar(320) COLLATE utf8mb4_bin NOT NULL COMMENT '메일 최대값',
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '이름',
  `password` binary(60) NOT NULL COMMENT '비밀번호',
  `create_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '생성 날짜',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='인증된 사용자\r\n';

CREATE TABLE IF NOT EXISTS 'notices' (
  'notice_id' bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'notice id',
  'author_id' bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'author id',
  'notice_title' varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT 'notice 타이틀',
  'notice_type' ENUM('title', 'topbar', 'message', 'none'),
  'notice_contents' varchar(655351) COLLATE utf8mb4_bin NOT NULL COMMENT 'notice 컨텐츠'
)

CREATE TABLE IF NOT EXISTS 'notice_views' (
  'notice_id' bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'notice id',
  'user_id' bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'user id',
  'read_at' datetime,
  'never_show' tinyint(1) unsigned NOT NULL COMMENT '보여짐의 유무'
)
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
