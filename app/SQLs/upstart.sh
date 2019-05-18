#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        create table IF NOT EXISTS public.authors (
        author_id varchar(64) not null,
       author_name varchar(255) default null,
       primary key (author_id));

    CREATE TABLE IF NOT EXISTS messages (
	    message_id character(64) NOT NULL,
	    "text" character varying(4000) DEFAULT NULL::character varying,
	    author_id character(64) DEFAULT NULL::bpchar,
	    source_id character(64) DEFAULT NULL::bpchar,
	    creation_date timestamp without time zone,
	    filename character varying(255) DEFAULT NULL::character varying,
	    inprogress_flag boolean DEFAULT false,
	    PRIMARY KEY(message_id)
    );

    create table IF NOT EXISTS  sources (
        source_id varchar(64) not null,
       source_name varchar(255) default null,
       primary key (source_id));

    create table IF NOT EXISTS  words (
        word_id char(64) not null,
       text varchar(4000) default null,
       creation_date timestamp default null,
       primary key (word_id));

    create table IF NOT EXISTS  wordsinword (
        mainword_id char(64) not null,
       subword_id char(64) not null,
       count int not null,
       primary key (mainword_id, subword_id));

    commit;
EOSQL
