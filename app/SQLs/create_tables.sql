create table IF NOT EXISTS public.authors (
    author_id varchar(64) not null,
   author_name varchar(255) default null,
   primary key (author_id)
);

create table IF NOT EXISTS  messages (
    message_id char(64) not null,
   text varchar(4000) default null,
   author_id char(64) default null,
   source_id char(64) default null,
   creation_date timestamp default null,
   filename varchar(255) default null,
   primary key (message_id)
);

create table IF NOT EXISTS  sources (
    source_id varchar(64) not null,
   source_name varchar(255) default null,
   primary key (source_id)
);

create table IF NOT EXISTS  words (
    word_id char(64) not null,
   text varchar(4000) default null,
   creation_date timestamp default null,
   primary key (word_id)
);

create table IF NOT EXISTS  wordsinword (
    mainword_id char(64) not null,
   subword_id char(64) not null,
   count int not null,
   primary key (mainword_id, subword_id)
);
commit;
