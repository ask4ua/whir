# -*- coding: utf-8 -*-
import os
import yaml
import sys

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

def get_texts():

    def read_text_from_file(filename):

        text=""
        try:
            logger.debug("Starting reading TEXT from file")
            streamTextFile = open(str(filename), mode='rt', encoding='utf-8')
            # cnt=0
            # ch=streamTextFile.read(1)
            # while ch!='':
            #    TEXT+=ch

            text = streamTextFile.read()

            logger.info("File " + str(filename) + " read - closing it")
            streamTextFile.close()

        except Exception as exc:
            print("File " + filename + "operations failed with exception:", os.strerror(exc.errno))

        return text

    for filename in sys.argv[1:]:
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

def analyze():
    for somemessage in whir.message.get_all_messages():
        if not somemessage.decomposed:
            somemessage.decompose()


def sync_to_db():
    pass

if __name__=='__main__':
    import logging.config
    logging.config.fileConfig('conf/logging.conf')
    logger = logging.getLogger('root')

    Configs.load(logger)

    logger.info("Starting collecting texts")
    get_texts()

    logger.info("Starting Analysis")
    analyze()

    logger.info("DB starting save to DB")
    db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'],
                    host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'],
                    database=Configs.actual_config['db_database'])

    db_session.sync_all_to_db()
    db_session.check_sync()

    db_session.close_db()
    logger.info("DB consistency check finished")

logger.info("Job is done")
