create database
    whir
    character set = utf8mb4
    collate = utf8mb4_unicode_ci;

use whir;

create table `authors` (
    `author_id` varchar(64) not null,
   `author_name` varchar(255) default null,
   primary key (`author_id`)
) engine = innodb default charset = utf8mb4;

create table `messages` (
    `message_id` char(64) not null,
   `text` varchar(4000) default null,
   `author_id` char(64) default null,
   `source_id` char(64) default null,
   `creation_date` datetime default null,
   `filename` varchar(255) default null,
   primary key (`message_id`)
) engine = innodb default charset = utf8mb4;

create table `sources` (
    `source_id` varchar(64) not null,
   `source_name` varchar(255) default null,
   primary key (`source_id`)
) engine = innodb default charset = utf8mb4;

create table `words` (
    `word_id` char(64) not null,
   `text` varchar(4000) default null,
   `creation_date` datetime default null,
   primary key (`word_id`)
) engine = innodb default charset = utf8mb4;

create table `wordsinword` (
    `mainword_id` char(64) not null,
   `subword_id` char(64) not null,
   `count` int(11) not null,
   primary key (`mainword_id`, `subword_id`)
) engine = innodb default charset = utf8mb4;

