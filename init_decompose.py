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
logger = logging.getLogger('init_decomposer')
Configs.load(logger)

while True:
    db_session = db(user=Configs.actual_config['db_user'], password=Configs.actual_config['db_password'],
                    host=Configs.actual_config['db_host'], port=Configs.actual_config['db_port'],
                    database=Configs.actual_config['db_database'])

    not_decomposed_list = db_session.get_not_decomposed_messages()

    db_session.close_db()

    cnt=0
    if len(not_decomposed_list)>0:
        file_cnt=0
        container_cnt=0
        file_limit=10
        container_limit=10
        files=""

        pause_time=600

        for file in not_decomposed_list:
            cnt+=1
            files += file + " "
            file_cnt+=1

            if file_cnt==file_limit-1 or cnt==len(not_decomposed_list):
                if container_cnt<container_limit:
                    os.system("nohup docker run --volumes-from whir-data --rm ubuntu1804py3 python3 decomposer.py " + str(files) + " &")
                    container_cnt += 1
                    logger.info("Start docker decomposer for files:" + str(files))
                else:
                    logger.info(str(container_cnt) + " containers started - sleeping for " + str(int(pause_time)) + " seconds to start next " + str(container_limit))
                    #container_cnt=0
                    break

                file_cnt = 0
                files=""

    time.sleep(600)