# -*- coding: utf-8 -*-
import os
import yaml
import sys

import whir.counter as whir
from whir.db import db
from whir.db import author
from whir.db import source

import csv
import time


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
        somemessage = whir.message(read_text_from_file(filename, logger))

    except BaseException as exc:
        logger.warning("File " + str(filename) + " not read because of: " + str(exc.__str__()))
        return False

    someauthor = whir.author.safe_create(author)
    somesource = whir.source.safe_create(source)

    somemessage.author_id = someauthor.id
    somemessage.source_id = somesource.id

    logger.info("File " + filename + " and it`s hash: " + somemessage.id)
    logger.info("Author: " + author + " hash: " + somemessage.author_id)
    logger.info("Source: " + source + " hash: " + somemessage.source_id)

    #try:
        #os_filename=filename.replace(" ","\\ ")
        #os.system("rm -rf " + os_filename)
        #logger.info("Sorce File removed; " + filename)
    #except:
        #logger.warning("Source File wasn`t removed")

    somemessage.filename = "/data/HASHED/" + somemessage.id + ".txt"
    write_text_to_file(somemessage.filename, somemessage.text, logger)

    return True


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

def parse_files_index(files_index,logger):
    author = ""
    source = ""
    filename = ""

    for i in range(len(files_index)):
        if files_index[i][0].lower()=='new':

            author=files_index[i][1]
            source=files_index[i][2]
            filename=files_index[i][3]

            if author != "" and source != "" and filename != "":
                if parse_message(author, source, filename, logger):
                    files_index[i][0]="parsed"
                else:
                    logger.warning("File " + str(filename) + " was skipped!")
                    files_index[i][0] = "skipped"
            else:
                files_index[i][0] = "some fields missed"



def connect_to_db():

    user=str(os.environ['WHIR_DB_USER'])
    database=str(os.environ['WHIR_DB_NAME'])
    host=str(os.environ['WHIR_DB_HOST'])
    filename = str(os.environ['WHIR_DB_PASSWORD_FILE'])
    passwd=read_text_from_file(filename,logger).strip()

    #logger.info("Whir: Host: "+ str(host) + " User: "+ str(user)+ " db: "+ str(database)+ " passwd: "+ str(passwd) +" ;" )
    db_session = db(user=user, password=passwd,host=host,database=database)

    return db_session

def readcsv(filename,logger):
    files_index=[]

    streamTextFile = open(str(filename), mode='rt', encoding='utf-8')

    try:
        row = streamTextFile.readline()
        while len(row) > 1:

            files_index.append(row.split('|')[0:4])
            row = streamTextFile.readline()

    except BaseException as exc:
        logger.warning("File " + filename + " cannot read some string: " + str(exc.__str__()))
        streamTextFile.close()

    streamTextFile.close()
    logger.info("File " + str(filename) + " read - closing it")

    logger.info(files_index)
    return files_index

def writecsv(files_index,filename,logger):

    text=""
    for row in files_index:
        for i in range(len(row)):
            text += row[i] + "|"
        text+="|\n"

    streamTextFile= open(str(filename), mode='wt',encoding='utf-8')
    try:
        streamTextFile.write(text)
    except BaseException as exc:
        logger.warning("File " + filename + " cannot write some string due to: " + str(exc.__str__()))
        logger.warning("String :" + str(row))
        streamTextFile.close()

    streamTextFile.close()

def sync_to_db():
    #db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'],
    #                host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'],
    #                database=Configs.actual_config['db_database'])

    logger.info("Total words:" + str(len(whir.word.get_all_ids())))
    logger.info("Total authors:" + str(len(whir.author.get_all_ids())))
    logger.info("Total sources:" + str(len(whir.source.get_all_ids())))
    logger.info("Total messages:" + str(len(whir.message.get_all_ids())))

    db_session = connect_to_db()

    db_session.sync_all_to_db()
    db_session.check_sync()

    db_session.close_db()
    logger.info("DB consistency check finished")

if __name__=='__main__':
    import logging.config
    logging.config.fileConfig('conf/logging.conf')
    logger = logging.getLogger('root')

    Configs.load(logger)

    logger.info("Reading Index CSV")
    files_index=readcsv('/data/index.csv',logger)

    logger.info("Parsing Input")
    parse_files_index(files_index,logger)

    logger.info("Updating CSV")
    writecsv(files_index, '/data/index.csv', logger)

    logger.info("Syncing to DB")
    sync_to_db()








