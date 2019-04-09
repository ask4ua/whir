# -*- coding: utf-8 -*-
from os import strerror
import logging.config
logging.config.fileConfig('conf/logging.conf')
logger = logging.getLogger('root')

import whir.counter as whir

TEXT=''
try:
    logger.debug("Starting reading TEXT from file")
    streamTextFile = open('text.txt',mode='rt',encoding='utf-8')
    #cnt=0
    #ch=streamTextFile.read(1)
    #while ch!='':
    #    TEXT+=ch

    TEXT=streamTextFile.read()

    logger.debug("File read - closing it")
    streamTextFile.close()

except Exception as exc:
    print("File operations failed with exception:", strerror(exc.errno))

message1=whir.message(TEXT)
print(message1.get_unified_text())

message1.decompose()
message1.print_all_words()

logger.info("Job is done")