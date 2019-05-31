# -*- coding: utf-8 -*-
import os
import yaml
import sys
import time
import random

import logging.config
logging.config.fileConfig('conf/logging.conf')
logger = logging.getLogger('decomposer')

import whir.counter as whir
from whir.db import db


class Configs:
    actual_config={}

    def load(logger):
        with open('conf/credentials.yaml', 'rt', encoding='utf-8') as ymlstream:
            cfg = yaml.safe_load(ymlstream)
            #cfg = yaml.load(ymlstream)

        logger.info("Actual config set: " + cfg['actual'])

        Configs.actual_config = cfg[cfg['actual']]



def read_text_from_file(filename):

    text=""
    try:
        logger.debug("Starting reading TEXT from file")
        streamTextFile = open(str(filename), mode='rt', encoding='utf-8')
        #streamTextFile = open(str(filename), mode='rt')
        # cnt=0
        # ch=streamTextFile.read(1)
        # while ch!='':
        #    TEXT+=ch

        text = streamTextFile.read()

        logger.info("File " + str(filename) + " read - closing it")
        streamTextFile.close()

    except Exception as exc:
        logger.warning("File " + filename + "operations failed with exception:", os.strerror(exc.errno))

    return text

def read_files(files):
    for filename in files:
        logger.debug("Input file: " + filename)
        message = whir.message(read_text_from_file(filename))

    #directory = os.fsencode("./texts/")
    #for file in os.listdir(directory):
    #     filename = os.fsdecode(file)
    #     if filename.endswith(".txt"):
    #         message = whir.message(read_text_from_file("./texts/"+filename))
    #         logger.debug("Read file: " + filename)
    #     else:
    #         continue

def connect_to_db():

    user=str(os.environ['WHIR_DB_USER'])
    database=str(os.environ['WHIR_DB_NAME'])
    host=str(os.environ['WHIR_DB_HOST'])
    filename = str(os.environ['WHIR_DB_PASSWORD_FILE'])
    passwd=read_text_from_file(filename).strip()
    
    #logger.info("Whir: Host: "+ str(host) + " User: "+ str(user)+ " db: "+ str(database)+ " passwd: "+ str(passwd) +" ;" )
    db_session = db(user=user, password=passwd,host=host,database=database)

    return db_session

def read_from_db(file_limit=10):
    #db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'],
    #                host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'],
    #                database=Configs.actual_config['db_database'])
    
    db_session = connect_to_db()
    not_decomposed_list = db_session.get_not_decomposed_messages(file_limit)
    db_session.close_db()

    return not_decomposed_list

def analyze():
    for somemessage in whir.message.get_all():
        if not somemessage.decomposed:
            somemessage.decompose()

def sync_to_db():
    #db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'],
    #                host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'],
    #                database=Configs.actual_config['db_database'])
    logger.info("Total words:" + str(len(whir.word.get_all_ids())))
    logger.info("Total authors:" + str(len(whir.author.get_all_ids())))
    logger.info("Total sources:" + str(len(whir.source.get_all_ids())))
    logger.info("Total messages:" + str(len(whir.message.get_all_ids())))

    while True:
        try:
            logger.info("Starting getting New word IDS from DB")

            db_session = connect_to_db()
            db_session.sync_all_to_db()

        except BaseException as exc:

            db_session.close_db()
            logger.error("Some exception during sync_to_db " + str(exc.__str__()))
            logger.info("Retrying to connect to db and sync")

            logger.info("Sleeping for 10 seconds before retry")
            time.sleep(10)

        else:
            logger.info("Writing to DB finished")
            break

    logger.info("Starting DB consistency checks after writing")

    while True:
        try:
            db_session = connect_to_db()
            db_session.check_sync()

            break
        except BaseException as exc:
            db_session.close_db()
            logger.error("Some exception during sync_to_db " + str(exc.__str__()))
            logger.info("Retrying to connect to db and check")

            logger.info("Sleeping for 10 seconds before retry")
            time.sleep(10)

        else:
            db_session.close_db()
            logger.info("DB consistency check finished")
            break

def remove_messages_from_db():
    db_session = connect_to_db()
    db_session.remove_messages_from_db()
    db_session.close_db()

def inprogress_messages(msg_ids):

    db_session = connect_to_db()
    db_session.inprogress_messages(msg_ids)
    db_session.close_db()

def clear_all():
    whir.message.clear_all()
    whir.author.clear_all()
    whir.source.clear_all()
    whir.word.clear_all()

if __name__=='__main__':
    Configs.load(logger)

    if len(sys.argv) > 1:
        logger.info("Starting reading of files: " + str(sys.argv[1:]))
        read_files(sys.argv[1:])

        logger.info("Starting Parsing and Analysis")
        analyze()

        logger.info("DB starting save to DB")
        sync_to_db()

    else:
        #while True:

        file_limit_per_1_thread = 1

        #timer to split simulteneously started instances
        pause_time = random.randint(1, 30)
        logger.info("Sleeping for " + str(pause_time) + " seconds.")

        logger.info("Starting getting not decomposed files list from DB")
        not_decomposed_ids_files_list=read_from_db(file_limit_per_1_thread)

        not_decomposed_ids_list=[]
        not_decomposed_files_list=[]

        for pair in not_decomposed_ids_files_list:
            not_decomposed_ids_list.append(pair[0])
            not_decomposed_files_list.append(pair[1])


        logger.info("Setting to edit in progress loaded messages from DB")
        # remove_messages_from_db()
        inprogress_messages(not_decomposed_ids_list)

        logger.info("Starting reading of files")
        read_files(not_decomposed_files_list)

        logger.info("Starting Parsing and Analysis")
        analyze()

        logger.info("DB starting save to DB")
        sync_to_db()

        #pause_time = 2
        #pause_time += random.randint(1, 30)

        #logger.info("Removing all decomposed entities for the next run")
        #whir.clear_all()

        #logger.info("Sleeping for " + str(pause_time) + " seconds.")
        #time.sleep(pause_time)

    logger.info("Job is done")
