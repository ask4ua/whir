import yaml
#from docker import Client as DockerClient
from whir.db import db
import os
import time

class Configs:
    actual_config={}

    def load(logger):
        with open('conf/credentials.yaml', 'rt', encoding='utf-8') as ymlstream:
            cfg = yaml.safe_load(ymlstream)
            #cfg = yaml.load(ymlstream)

        logger.info("Actual config set: " + cfg['actual'])

        Configs.actual_config = cfg[cfg['actual']]

import logging.config
logging.config.fileConfig('conf/logging.conf')
logger = logging.getLogger('root')
Configs.load(logger)

db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'],
                    host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'],
                    database=Configs.actual_config['db_database'])

not_decomposed_list=db_session.get_not_decomposed_messages()

if len(not_decomposed_list)>0:

    cnt=0
    limit=100
    for file in not_decomposed_list:
        logger.info("Command to start docker, file:" + str(file))
        os.system("nohup docker run --volumes-from whir-data --rm ubuntu1804py3 python3 decompose_messages.py " + str(file) +" &")
        #os.system("docker run -v /Users/volk/Downloads/txt/:/data -v /Users/volk/GIT/whir/:/app --rm ubuntu18.04py3 ls ./")
        
        cnt+=1
        if cnt >= limit:
            time.sleep(3600)
            logger.info(str(limit) + " containers started - sleeping for 1 hout to start next 10")

db_session.close_db()

