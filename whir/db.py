import mysql.connector
import re
import datetime


from whir.counter import word
from whir.counter import message

from mysql.connector import errorcode

import logging.config
logger = logging.getLogger('db')

import time

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
    def delete_words(word_ids):

        SQL = "delete from words where word_id in ("
        for word_id in word_ids:
            SQL+="\'" + str(word_id) + "\', "

        SQL = SQL[0:-2]
        SQL += ");"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def insert_words(word_ids, date):

        SQL = "insert into words (word_id, text, creation_date) values"
        for someword_id in word_ids:
            someword=word.get_by_id(someword_id)
            SQL+="(\'" + str(someword.id) + "\', \'" + queries.masking(someword.unified_text[0:4000]) + "\', \'" + str(date) + "\'), "

        SQL = SQL[0:-2]
        SQL += ";"

        logger.debug("SQL: " + str(SQL))
        return SQL

    def delete_wordsinword(word_id):
        SQL = "delete from wordsinword where mainword_id=\'" + str(word_id) + "\';"
        logger.debug("SQL: "+SQL)
        return SQL

    @staticmethod
    def insert_word_in_word(word_id):
        someword = word.get_by_id(word_id)
        SQL=""
        if someword.get_subwords():
            SQL += "insert into wordsinword (mainword_id,subword_id,count) values "
            for subword_id,count in someword.get_subwords():
                SQL += "(\'" + str(word_id) + "\', \'" + str(subword_id) + "\', \'" + str(count) + "\'), "

            SQL=SQL[0:-2]
            SQL+=";"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def insert_wordsinwords(word_ids):
        SQL = ""
        count=0
        for word_id in word_ids:
            someword = word.get_by_id(word_id)
            if someword.get_subwords():
                count+=1
                if count==1:
                    SQL += "insert into wordsinword (mainword_id,subword_id,count) values "

                for subword_id, count in someword.get_subwords():
                    SQL += "(\'" + str(word_id) + "\', \'" + str(subword_id) + "\', \'" + str(count) + "\'), "

        if count>0:
            SQL = SQL[0:-2]
            SQL += ";"

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

    @staticmethod
    def get_existing_word_ids(word_ids):

        SQL="select word_id from words where word_id in("
        for word_id in word_ids:
            SQL+='\'' + str(word_id)+ '\', '
        SQL=SQL[0:-2]
        SQL+=');'
        return SQL

    @staticmethod
    def create_temp_table_word_id():

        #SQL = "create temporary table new_word_ids (word_id char(64));"
        SQL = "create table new_word_ids (word_id char(64));"
        logger.debug(SQL)
        return SQL

    @staticmethod
    def fill_in_temp_table_word_id(word_ids):
        SQL = "INSERT INTO new_word_ids values "
        for word_id in word_ids:
            SQL += '(\'' + str(word_id) + '\'), '
        SQL = SQL[0:-2]
        SQL += ';'
        return SQL

    @staticmethod
    def get_new_word_ids_with_temp_table():

        SQL="SELECT new_word_ids.word_id FROM words right JOIN new_word_ids ON \
            new_word_ids.word_id=words.word_id where words.word_id is Null;"

        return SQL

    @staticmethod
    def drop_new_word_ids_temp_table():
        SQL="drop table new_word_ids;"
        return SQL


    @staticmethod
    def get_new_words_ids_in_one_try(word_ids):
        SQL=""
        SQL += "create temporary table new_word_ids (word_id char(64));"
        SQL += "INSERT INTO new_word_ids values "
        for word_id in word_ids:
            SQL += '(\'' + str(word_id) + '\'), '
        SQL = SQL[0:-2]
        SQL += ';'

        SQL += "SELECT new_word_ids.word_id FROM words right JOIN new_word_ids ON \
                    new_word_ids.word_id=words.word_id where words.word_id is Null;"

        SQL += "drop table new_word_ids;"

        return SQL

    @staticmethod
    def get_count_by_word_ids(word_ids):

        SQL = "SELECT sum(wordsinword.count) \"total\" from wordsinword where mainword_id in ("
        for word_id in word_ids:
            SQL+='\''+str(word_id)+'\', '

        SQL=SQL[0:-2]
        SQL+=');'

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

        def get_new_words(all_word_ids, sql_session):
            new_word_ids=[]

            cursor = sql_session.cursor()
            iterator=cursor.execute(queries.get_new_words_ids_in_one_try(all_word_ids),multi=True)

            try:
                for result in iterator:
                    if result.with_rows:
                        for somearray in result.fetchall():
                            for sometuple in somearray:
                                new_word_ids.append(str(sometuple))

            except RuntimeError:
                logger.warning("No words ids to insert found!. Ok for the case of failed new word ids collecting;)")

            cursor.close()
            return new_word_ids


        def write_word_to_db(new_word_ids,sql_session,date):
            logger.info("Starting words only to DB")

            cursor = sql_session.cursor()
            db_parser.force_utf8mb4(cursor)
            # mysql.connector.errors.IntegrityError: 1062 (23000): Duplicate entry '83c01...e7b5' for key 'PRIMARY'
            # in such case repeat new words and try again

            try:
                cursor.execute(queries.insert_words(new_word_ids, date))

            except mysql.connector.Error as err:
                logger.warning("Retrying procedure of defining new words while catched: " + str(err.__str__() + " " + str(err.errno)))
                cursor.close()
                time.sleep(10)

                return False
            else:
                sql_session.commit()
                cursor.close()
                return True

        def write_wordsinword_to_db(new_word_ids,sql_session):
            logger.info("Starting wordsinword to DB")
            cursor = sql_session.cursor()
            db_parser.force_utf8mb4(cursor)

            for word_id in new_word_ids:
                cursor.execute(queries.insert_word_in_word(word_id))

            sql_session.commit()
            cursor.close()

            return True

        words_synced=False
        all_word_ids = word.get_all_words_ids()

        while not words_synced:
            new_word_ids=get_new_words(all_word_ids,sql_session)
            logger.info("Total words in this run: " + str(len(all_word_ids)) + ", new word_ids : " + str(len(new_word_ids)))

            if len(new_word_ids) == 0:
                break
            else:
                logger.info("Starting writing to DB all new words")

                words_synced = write_word_to_db(new_word_ids,sql_session,date)
                if not words_synced:
                    continue

                words_synced = write_wordsinword_to_db(new_word_ids, sql_session)



            #consistence check:

    @staticmethod
    def check_save_consistency_words(sql_session):
        WAIT_TIMER=5 #minutes

        app_subwords_count=0
        for someword in word.get_all_words():
            for subword_id,count in someword.get_subwords():
                app_subwords_count+=int(count)

        check_status=False
        all_word_ids = word.get_all_words_ids()

        while not check_status:

            db_subwords_count = -1

            cursor = sql_session.cursor()
            db_parser.force_utf8mb4(cursor)
            cursor.execute(queries.get_count_by_word_ids(all_word_ids))

            for result in cursor:
                db_subwords_count=int(result[0])


            cursor.close()


            check_status=(db_subwords_count==app_subwords_count)

            if check_status:
                logger.info("Consistency check PASSED: db subwords=" + str(db_subwords_count) + " = app subowrds = " + str(app_subwords_count))

            else:
                logger.error("FAILED DB Consistency check: db subwords=" + str(db_subwords_count) + " and app subowrds = " + str(app_subwords_count))
                logger.error("Waiting for " + str(WAIT_TIMER) +" minutes - and rechecking again - possibly some other sessions have not finished!")

                time.sleep(WAIT_TIMER*60)


    @staticmethod
    def sync_all_messages_to_db(sql_session,date):

        logger.info("Starting creating in DB messages")
        cursor = sql_session.cursor()
        db_parser.force_utf8mb4(cursor)

        for message_id in message.get_by_id():
            cursor.execute(queries.safe_message_create(message_id))
            cursor.execute(queries.update_message(message_id, date))

        sql_session.commit()

        cursor.close()


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

    def check_sync(self):
        db_parser.check_save_consistency_words(self.sql_session)


    def close_db(self):
        self.sql_session.close()
        logger.info("DB connection closed")