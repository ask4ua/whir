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
        
    streamTextFile = open(str(filename), mode='rt')

    ch="Start"
    while ch != '':
        try:
            ch=streamTextFile.read(1)
            text+=ch

        except BaseException as exc:
            logger.warning("File " + filename + " cannot read some char" + str(exc.__str__()))
            ch="continue"
            continue

    logger.info("File " + str(filename) + " read - closing it")
    streamTextFile.close()

    return text

def write_text_to_file(filename,text,logger):
    file=open(str(filename),"wt")
    file.write(text)
    file.close()

    logger.info("File " + filename + " is written.")


def parse_message(author,source,filename,logger):
    logger.info("Input file: " + filename)

    try:
        message = whir.message(read_text_from_file(filename, logger))

    except BaseException:
        logger.warning("File " + str(filename) + " not read!")
        return False

    message.calculate_id()

    someauthor = whir.author.safe_create(author)
    somesource = whir.source.safe_create(source)

    message.author_id = someauthor.id
    message.source_id = somesource.id

    logger.info("File " + filename + " and it`s hash: " + message.id)
    logger.info("Author: " + author + " hash: " + message.author_id)
    logger.info("Source: " + source + " hash: " + message.source_id)

    #try:
        #os_filename=filename.replace(" ","\\ ")
        #os.system("rm -rf " + os_filename)
        #logger.info("Sorce File removed; " + filename)
    #except:
        #logger.warning("Source File wasn`t removed")

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
            if not parse_message(author, source, filename, logger):
                logger.warning("Skippimg File " + str(filename))


if __name__=='__main__':
    import logging.config
    logging.config.fileConfig('conf/logging.conf')
    logger = logging.getLogger('create_message')

    Configs.load(logger)

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