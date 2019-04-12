import mysql.connector
import re
import datetime

from whir.counter import word
from whir.counter import message

from mysql.connector import errorcode

import logging.config
logger = logging.getLogger('db')


class queries:

    @staticmethod
    def masking(text):
        masking_rules={
            '\'':'\\\'',
            '"':'\\\"',
            '%':'\\%',
            '(': '\\(',
            ')': '\\)',
            '[': '\\]',
            '[': '\\]',

        }

        logger.debug("Text before masking:" + text)

        for symbol,swap_symbol in masking_rules.items():
            text=text.replace(symbol,swap_symbol)

        logger.debug("Text after masking:" + text)

        return text



    @staticmethod
    def sql_injection_protection(element):
        key_words=['select','drop','insert','delete','describe']

        for word in key_words:
            if word.upper() in element.upper:
                logger.warning("SQL Injection detected in input %s" % (element))

                insensitive_replace= re.compile(re.escape(word), re.IGNORECASE)
                element = insensitive_replace.sub('',element)

        return element

    @staticmethod
    def safe_word_create(word_id):
        SQL = "insert into words (word_id) select \'" + str(word_id) + "\' from dual where not exists (select 1 from words where word_id = \'" + str(word_id) + "\');"
        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def safe_message_create(message_id):
        SQL = "insert into messages (message_id) select \'" + str(message_id) + "\' from dual where not exists (select 1 from messages where message_id = \'" + str(message_id) + "\');"
        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def update_word(word_id, date):
        someword=word.get_by_id(word_id)

        SQL="update words set \
            text= \'" + queries.masking(someword.unified_text[0:4000]) + "\', \
            creation_date = \'" + str(date) + "\' \
            where word_id=\'" + str(word_id) + "\';"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def update_word_in_word(word_id):
        someword=word.get_by_id(word_id)

        SQL = "delete from wordsinword where mainword_id=" + str(word_id) + ";"
        if someword.get_subwords():
            SQL += "insert wordsinword (mainword_id,subword_id,count) values "
            for subword_id,count in someword.get_subwords():
                SQL += "(mainword_id=\'" + str(word_id) + "\', subword_id=\'" + str(subword_id) + "\', count=\'" + str(count) + "\'), "

            SQL=SQL[0:-2]
            SQL+=";"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def update_message(message_id,date):
        somemessage=message.get_by_id(message_id)

        SQL="update messages set \
            text= \'" + queries.masking(somemessage.unified_text[0:4000]) + "\', \
            creation_date = \'" + str(date) + "\' \
            where message_id=\'" + str(message_id) + "\';"

        logger.debug("SQL: " + str(SQL))
        return SQL


class db_parser:

    @staticmethod
    def force_utf8mb4(cursor):
        cursor.execute('SET NAMES utf8mb4;')
        cursor.execute("SET CHARACTER SET utf8mb4;")
        cursor.execute("SET character_set_connection=utf8mb4;")

    @staticmethod
    def sync_all_words_to_db(sql_session, date):

        logger.debug("Staring saving all words to db")

        SQL = ""

        cursor = sql_session.cursor()
        db_parser.force_utf8mb4(cursor)

        for word_id in word.sort_by_subwords_and_get_word_ids():
            SQL=""

            cursor.execute(queries.safe_word_create(word_id))
            cursor.execute(queries.update_word(word_id, date))
            cursor.execute(queries.update_word_in_word(word_id),multi=True)

        sql_session.commit()

        cursor.close()



        #cursor = sql_session.cursor()
        ##
        #cursor.execute(SQL)
        #sql_session.commit()


        return SQL

    @staticmethod
    def sync_all_messages_to_db(sql_session,date):

        SQL = ""

        cursor = sql_session.cursor()
        db_parser.force_utf8mb4(cursor)

        for message_id in message.get_by_id():
            cursor.execute(queries.safe_message_create(message_id))
            cursor.execute(queries.update_message(message_id, date))

        logger.info("SQL for sync_all_words_to_db length:" + str(len(SQL)))



        #cursor.execute(SQL, multi=True)
        sql_session.commit()

        cursor.close()
        return SQL


class db:

    def __init__(self, **db_options):

        try:
            self.sql_session = mysql.connector.connect(user=db_options.get('user'), password=db_options.get('password'), host=db_options.get('host'), port=db_options.get('port'), database=db_options.get('database'), use_unicode=True)
            logger.info("Openning new DB connection")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("DB ERROR: Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("DB ERROR: Database does not exist")


            else:
                logger.error(err)

    def sync_all_to_db(self):
        time_now = datetime.datetime.now()
        date = time_now.strftime('%Y-%m-%d %H:%M:%S')

        db_parser.sync_all_words_to_db(self.sql_session,date)
        db_parser.sync_all_messages_to_db(self.sql_session,date)


    def close_db(self):
        self.sql_session.close()
        logger.info("DB connection closed")