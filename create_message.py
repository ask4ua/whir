# -*- coding: utf-8 -*-
import os
import yaml
import sys

import whir.counter as whir
from whir.db import db
from whir.db import author
from whir.db import source


#author,book name, file

class Configs:
    actual_config={}

    def load(logger):
        with open('conf/credentials.yaml', 'rt', encoding='utf-8') as ymlstream:
            cfg = yaml.safe_load(ymlstream)
            #cfg = yaml.load(ymlstream)

        logger.info("Actual config set: " + cfg['actual'])

        Configs.actual_config = cfg[cfg['actual']]


def read_text_from_file(filename,logger):

    text=""
    #try:
    logger.debug("Starting reading TEXT from file")

    try:
        streamTextFile = open(str(filename), mode='rt', encoding='utf-8')

        ch="Start"
        while ch != '':
            try:
                ch=streamTextFile.read(1)
                text+=ch

            except BaseException as exc:
                logger.warning("File " + filename + " cannot read some char")
                ch="continue"
                continue

    except BaseException as exc:
        logger.warning("File " + filename + " cannot read with exception: " + os.strerror(exc.errno))
    else:
        logger.info("File " + str(filename) + " read - closing it")
        streamTextFile.close()
        #text = streamTextFile.read()


        #except Exception as exc:
        #    print("File " + filename + "operations failed with exception:", os.strerror(exc.errno))

    return text

def write_text_to_file(filename,text,logger):
    file=open(str(filename),"wt")
    file.write(text)
    file.close()

    logger.info("File " + filename + " is written.")


def parse_message(author,source,filename,logger):
    logger.info("Input file: " + filename)

    message = whir.message(read_text_from_file(filename, logger))
    message.calculate_id()

    someauthor = whir.author.safe_create(author)
    somesource = whir.source.safe_create(source)

    message.author_id = someauthor.id
    message.source_id = somesource.id

    logger.info("File " + filename + " and it`s hash: " + message.id)
    logger.info("Author: " + author + " hash: " + message.author_id)
    logger.info("Source: " + source + " hash: " + message.source_id)

    os.system("rm -rf " + filename)
    logger.info("Sorce File removed; " + filename)

    message.filename = "/data/HASHED/" + message.id + ".txt"
    write_text_to_file(message.filename, message.text, logger)


def parse_input(logger):
    author = ""
    source = ""
    filename = ""
    logger.info("Input arguments:" + str(sys.argv))

    for index in range(1,len(sys.argv)):

        if sys.argv[index]=="-a":
            index += 1
            author = sys.argv[index]
        elif sys.argv[index]=="-s":
            index += 1
            source = sys.argv[index]
        elif sys.argv[index]=="-f":
            index += 1
            filename = sys.argv[index]
        #else:
        #    logger.warning("The input argument " + str(index+1) + " not parsed:" + sys.argv[index])
        #    logger.info("Parsed arguments: file:" + filename + " author: " + author + " source:" + source)
        #    exit(1)


        if author!="" and source!="" and filename!="":
            parse_message(author, source, filename, logger)
            filename=""
    else:
        return False

def parse_files(files,logger):
    author = ""
    source = ""
    filename = ""

    for author,source,filename in files:
        if author != "" and source != "" and filename != "":
            parse_message(author, source, filename, logger)


if __name__=='__main__':
    import logging.config
    logging.config.fileConfig('conf/logging.conf')
    logger = logging.getLogger('create_message')

    Configs.load(logger)

    author=""
    source=""

    logger.info("Parsing Input")
    if not parse_input(logger):
        from files import files
        if len(files)>0:
            parse_files(files,logger)


    db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'],
                    host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'],
                    database=Configs.actual_config['db_database'])

    db_session.sync_all_to_db()
    db_session.check_sync()

    db_session.close_db()