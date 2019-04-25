ALTER DATABASE
    whir
    CHARACTER SET = utf8mb4
    COLLATE = utf8mb4_unicode_ci;

CREATE TABLE `AUTHORS` (
    `AUTHOR_ID` VARCHAR(64) NOT NULL,
	`AUTHOR_NAME` VARCHAR(255) DEFAULT NULL,
	PRIMARY KEY (`AUTHOR_ID`)
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;

CREATE TABLE `MESSAGES` (
    `MESSAGE_ID` CHAR(64) NOT NULL,
	`TEXT` VARCHAR(4000) DEFAULT NULL,
	`AUTHOR_ID` CHAR(64) DEFAULT NULL,
	`SOURCE_ID` CHAR(64) DEFAULT NULL,
	`CREATION_DATE` DATETIME DEFAULT NULL,
	`FILENAME` VARCHAR(255) DEFAULT NULL,
	PRIMARY KEY (`MESSAGE_ID`)
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;

CREATE TABLE `SOURCES` (
    `SOURCE_ID` VARCHAR(64) NOT NULL,
	`SOURCE_NAME` VARCHAR(255) DEFAULT NULL,
	PRIMARY KEY (`SOURCE_ID`)
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;

CREATE TABLE `WORDS` (
    `WORD_ID` CHAR(64) NOT NULL,
	`TEXT` VARCHAR(4000) DEFAULT NULL,
	`CREATION_DATE` DATETIME DEFAULT NULL,
	PRIMARY KEY (`WORD_ID`)
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;

CREATE TABLE `WORDSINWORD` (
    `MAINWORD_ID` CHAR(64) NOT NULL,
	`SUBWORD_ID` CHAR(64) NOT NULL,
	`COUNT` INT(11) NOT NULL,
	PRIMARY KEY (`MAINWORD_ID`, `SUBWORD_ID`)
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;