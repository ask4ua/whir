# -*- coding: utf-8 -*-
import os
import yaml

import whir.counter as whir
from whir.db import db

import logging.config
logging.config.fileConfig('conf/logging.conf')
logger = logging.getLogger('root')

class Configs:
    actual_config={}

    def load(logger):
        with open('conf/credentials.yaml', 'rt', encoding='utf-8') as ymlstream:
            cfg = yaml.safe_load(ymlstream)
            #cfg = yaml.load(ymlstream)

        logger.info("Actual config set: " + cfg['actual'])

        Configs.actual_config = cfg[cfg['actual']]

Configs.load(logger)

db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'], host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'], database=Configs.actual_config['db_database'])
#db_session.load_all_from_db()






def read_text_from_file(filename):
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



directory = os.fsencode("./")

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".txt"):
         message = whir.message(read_text_from_file(filename))
     else:
         continue

for somemessage in whir.message.get_all_messages():
    somemessage.decompose()

whir.word.print_all_words()

logger.info("Job is done")