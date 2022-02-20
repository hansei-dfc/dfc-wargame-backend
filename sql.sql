/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `war-game` /*!40100 DEFAULT CHARACTER SET armscii8 COLLATE armscii8_bin */;
USE `war-game`;

CREATE TABLE IF NOT EXISTS `notices` (
  `notice_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'notice id',
  `author_id` bigint(20) unsigned NOT NULL COMMENT '작성자',
  `notice_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '타이틀',
  `notice_contents` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '콘텐츠',
  `notice_type` enum('title','topbar','message','none') COLLATE armscii8_bin NOT NULL COMMENT '타입',
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '작성 날짜, 수정 날짜',
  PRIMARY KEY (`notice_id`)
) ENGINE=MyISAM DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin COMMENT='notices';

CREATE TABLE IF NOT EXISTS `notice_views` (
  `notice_id` bigint(20) unsigned NOT NULL COMMENT 'notice id',
  `user_id` bigint(20) unsigned NOT NULL COMMENT '사용자 id',
  `read_at` datetime NOT NULL COMMENT '읽은 날짜',
  `never_show` tinyint(1) unsigned NOT NULL COMMENT '다시 보지 않기'
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin COMMENT='notice 뷰 기록';

CREATE TABLE IF NOT EXISTS `problems` (
  `problem_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '문제 id',
  `author_id` bigint(20) unsigned NOT NULL COMMENT '작성자 id',
  `problem_tags` varchar(512) COLLATE utf8mb4_bin NOT NULL COMMENT '문제 태그 '';''로 split',
  `problem_title` varchar(512) COLLATE utf8mb4_bin NOT NULL COMMENT '문제 타이틀',
  `problem_difficulty` tinyint(3) unsigned NOT NULL COMMENT '문제 난이도',
  `problem_contents` text COLLATE utf8mb4_bin NOT NULL COMMENT '문제 콘텐츠',
  `problem_class` varchar(127) COLLATE utf8mb4_bin NOT NULL COMMENT '문제 클래스',
  `problem_score` smallint(5) unsigned NOT NULL COMMENT '문제 점수',
  `problem_format_id` bigint(20) unsigned NOT NULL COMMENT '포맷 id',
  `problem_created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '만들어진 날짜',
  `problem_updated_at` datetime DEFAULT NULL COMMENT '수정된 날짜',
  PRIMARY KEY (`problem_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='문제';

CREATE TABLE IF NOT EXISTS `problem_formats` (
  `problem_format_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '문제 포맷 id',
  `author_id` bigint(20) unsigned NOT NULL COMMENT '작성자 id',
  `problem_format_name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '문제 포멧 id',
  `problem_type` enum('find_flag','baekjoon','scorer') CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL COMMENT '문제 채점 타입',
  `problem_format_contents` text COLLATE utf8mb4_bin DEFAULT NULL COMMENT '문제 채첨 콘텐츠',
  `problem_format_parameter` text COLLATE utf8mb4_bin DEFAULT NULL COMMENT '문제 채점 파라미터',
  PRIMARY KEY (`problem_format_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='문제 채점 방식';

CREATE TABLE IF NOT EXISTS `problem_scoring` (
  `problem_scoring_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '채점 id',
  `player_id` bigint(20) unsigned NOT NULL COMMENT '플레이어 id',
  `scorer_id` bigint(20) unsigned DEFAULT NULL COMMENT '채점자 id',
  `problem_id` bigint(20) unsigned NOT NULL COMMENT '문제 id',
  `problem_format_id` bigint(20) unsigned NOT NULL COMMENT '문제 포맷 id',
  `contents` text COLLATE utf8mb4_bin NOT NULL COMMENT '콘텐츠',
  `score` smallint(5) unsigned NOT NULL COMMENT '점수',
  `scoring_status` enum('pending','waiting','get_right','wrong','time_out','resource_out') CHARACTER SET ascii COLLATE ascii_bin NOT NULL COMMENT '채첨 상태',
  `result_message` text COLLATE utf8mb4_bin NOT NULL COMMENT '채첨 결과 메시지',
  `request_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '요청 날짜',
  `scoring_at` datetime DEFAULT NULL COMMENT '채점 날짜',
  PRIMARY KEY (`problem_scoring_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='문제 채점';

CREATE TABLE IF NOT EXISTS `temp_users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '고유 id',
  `email` varchar(320) COLLATE utf8mb4_bin NOT NULL COMMENT '이메일 최대값',
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '이름',
  `password` binary(60) NOT NULL COMMENT '비밀번호',
  `verify_code` varchar(32) COLLATE utf8mb4_bin NOT NULL COMMENT '인증코드',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '고유id',
  `email` varchar(320) COLLATE utf8mb4_bin NOT NULL COMMENT '메일 최대값',
  `name` varchar(255) COLLATE utf8mb4_bin NOT NULL COMMENT '이름',
  `password` binary(60) NOT NULL COMMENT '비밀번호',
  `create_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '생성 날짜',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `name` (`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='인증된 사용자\r\n';

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
