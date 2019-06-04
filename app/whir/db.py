import mysql.connector
import psycopg2
import re
import datetime
import random


from whir.counter import word
from whir.counter import message
from whir.counter import source
from whir.counter import author

from mysql.connector import errorcode

import logging.config
logger = logging.getLogger('db')

import time

class queries:

    @staticmethod
    def masking(text):
        masking_rules={
            '\\': '\\\\',
            '\'':'\\\`',
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

    # @staticmethod
    # def safe_author_create(author_id):
    #     SQL = "insert into authors (author_id) select \'" + str(author_id) + "\' from dual where not exists (select 1 from authors where author_id = \'" + str(author_id) + "\');"
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def safe_source_create(source_id):
    #     SQL = "insert into sources (source_id) select \'" + str(source_id) + "\' from dual where not exists (select 1 from sources where source_id = \'" + str(source_id) + "\');"
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def safe_word_create(word_id):
    #     SQL = "insert into words (word_id) select \'" + str(word_id) + "\' from dual where not exists (select 1 from words where word_id = \'" + str(word_id) + "\');"
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def safe_message_create(message_id):
    #     SQL = "insert into messages (message_id) select \'" + str(message_id) + "\' from dual where not exists (select 1 from messages where message_id = \'" + str(message_id) + "\');"
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def update_author(author_id, date):
    #
    #     someauthor = author.get_by_id(author_id)
    #
    #     SQL = "update authors set \
    #             author_name= \'" + queries.masking(someauthor.name) + "\' \
    #             where author_id=\'" + str(author_id) + "\';"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def update_source(source_id, date):
    #     somesource = source.get_by_id(source_id)
    #
    #     SQL = "update sources set \
    #             source_name= \'" + queries.masking(somesource.name) + "\' \
    #             where source_id=\'" + str(source_id) + "\';"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def update_word(word_id, date):
    #     someword=word.get_by_id(word_id)
    #
    #     SQL="update words set \
    #         text= \'" + queries.masking(someword.unified_text[0:255]) + "\', \
    #         creation_date = \'" + str(date) + "\' \
    #         where word_id=\'" + str(word_id) + "\';"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def delete_words(word_ids):
    #
    #     SQL = "delete from words where word_id in ("
    #     for word_id in word_ids:
    #         SQL+="\'" + str(word_id) + "\', "
    #
    #     SQL = SQL[0:-2]
    #     SQL += ");"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def insert_words(word_ids, date, table_name="words"):
    #
    #     SQL = "insert into "+ str(table_name) +" (word_id, text, creation_date) values"
    #     for someword_id in word_ids:
    #         someword=word.get_by_id(someword_id)
    #         SQL+="(\'" + str(someword.id) + "\', \'" + queries.masking(someword.unified_text[0:255]) + "\', \'" + str(date) + "\'), "
    #
    #     SQL = SQL[0:-2]
    #     SQL += ";"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    # def delete_wordsinword(word_id):
    #     SQL = "delete from wordsinword where mainword_id=\'" + str(word_id) + "\';"
    #     logger.debug("SQL: "+SQL)
    #     return SQL
    #
    # @staticmethod
    # def insert_wordsinword(word_ids,table_name="wordsinword"):
    #     SQL=""
    #
    #     wordsinword_list=[]
    #     for word_id in word_ids:
    #         someword = word.get_by_id(word_id)
    #         if someword.get_subwords():
    #             for subword_id, count in someword.get_subwords():
    #                 wordsinword_list.append([str(word_id),str(subword_id),str(count)])
    #
    #     if len(wordsinword_list) > 0:
    #         SQL += "insert into "+ table_name +" (mainword_id,subword_id,count) values "
    #         for record in wordsinword_list:
    #             SQL += "(\'" + record[0] + "\', \'" + record[1] + "\', \'" + record[2] + "\'), "
    #
    #         SQL=SQL[0:-2]
    #         SQL+=";"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    # @staticmethod
    # def insert_wordsinwords(word_ids):
    #     SQL = ""
    #     count=0
    #     for word_id in word_ids:
    #         someword = word.get_by_id(word_id)
    #         if someword.get_subwords():
    #             count+=1
    #             if count==1:
    #                 SQL += "insert into wordsinword (mainword_id,subword_id,count) values "
    #
    #             for subword_id, count in someword.get_subwords():
    #                 SQL += "(\'" + str(word_id) + "\', \'" + str(subword_id) + "\', \'" + str(count) + "\'),\n"
    #
    #     if count>0:
    #         SQL = SQL[0:-2]
    #         SQL += ";"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL
    #
    #
    # @staticmethod
    # def update_message(message_id,date):
    #     somemessage=message.get_by_id(message_id)
    #
    #     SQL="update messages set \
    #         text= \'" + queries.masking(somemessage.unified_text[0:255]) + "\',"
    #
    #     if somemessage.author_id!="":
    #         SQL += "author_id = \'" + str(somemessage.author_id) + "\',"
    #     if somemessage.source_id!="":
    #         SQL += "source_id = \'" + str(somemessage.source_id) + "\',"
    #
    #     if somemessage.source_id!="":
    #         SQL += "filename = \'" + str(somemessage.filename) + "\',"
    #
    #     SQL+="creation_date = \'" + str(date) + "\' \
    #         where message_id=\'" + str(message_id) + "\';"
    #
    #     logger.debug("SQL: " + str(SQL))
    #     return SQL

    # @staticmethod
    # def get_existing_word_ids(word_ids):
    #
    #     SQL = "select word_id from words where word_id in("
    #     for word_id in word_ids:
    #         SQL += '\'' + str(word_id) + '\', '
    #     SQL = SQL[0:-2]
    #     SQL += ');'
    #     return SQL
    #
    # @staticmethod
    # def create_temp_table_word_id():
    #
    #     # SQL = "create temporary table new_word_ids (word_id char(64));"
    #     SQL = "create table new_word_ids (word_id char(64));"
    #     logger.debug(SQL)
    #     return SQL
    #
    # @staticmethod
    # def fill_in_temp_table_word_id(word_ids):
    #     SQL = "INSERT INTO new_word_ids values "
    #     for word_id in word_ids:
    #         SQL += '(\'' + str(word_id) + '\'), '
    #     SQL = SQL[0:-2]
    #     SQL += ';'
    #     return SQL
    #
    # @staticmethod
    # def get_new_word_ids_with_temp_table():
    #
    #     SQL = "SELECT new_word_ids.word_id FROM words right JOIN new_word_ids ON \
    #         new_word_ids.word_id=words.word_id where words.word_id is Null;"
    #
    #     return SQL
    #
    # @staticmethod
    # def drop_new_word_ids_temp_table():
    #     SQL = "drop table new_word_ids;"
    #     return SQL
    #
    @staticmethod
    def get_new_words_ids_create(word_ids):
        SQL = "create temporary table new_word_ids (word_id char(64));"
        SQL += "INSERT INTO new_word_ids values "
        for word_id in word_ids:
            SQL += '(\'' + str(word_id) + '\'),\n'
        SQL = SQL[0:-2]
        SQL += ';'

        return SQL

    @staticmethod
    def get_new_words_ids_select():

        SQL = "SELECT new_word_ids.word_id FROM words right JOIN new_word_ids ON \
                        new_word_ids.word_id=words.word_id where words.word_id is Null;"
        return SQL

    @staticmethod
    def get_new_words_ids_drop():
        SQL = "drop table new_word_ids;"

        return SQL

    @staticmethod
    def get_new_words_ids_in_one_try(word_ids):
        SQL = ""
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
    #
    # @staticmethod
    # def create_new_words_table(table_name):
    #     SQL = "create table " + str(
    #         table_name) + " (`WORD_ID` CHAR(64) NOT NULL,  `TEXT` VARCHAR(4000) DEFAULT NULL, `CREATION_DATE` DATETIME DEFAULT NULL, PRIMARY KEY (`WORD_ID`)) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4"
    #     return SQL
    #
    # @staticmethod
    # def create_new_wordsinword_table(table_name):
    #     SQL = "create table " + str(
    #         table_name) + " (`MAINWORD_ID` CHAR(64) NOT NULL, `SUBWORD_ID` CHAR(64) NOT NULL, `COUNT` INT(11) NOT NULL, PRIMARY KEY (`MAINWORD_ID`, `SUBWORD_ID`)) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4"
    #     return SQL
    #
    # @staticmethod
    # def merge_the_tables(src_table, dst_table):
    #     SQL = "INSERT IGNORE " + "INTO " + str(dst_table) + " SELECT * FROM " + str(src_table) + ";"
    #     return SQL
    #
    # @staticmethod
    # def drop_the_table(table_name):
    #     SQL = "drop table " + str(table_name) + ";"
    #     return SQL

    @staticmethod
    def get_not_decomposed_message_files(file_limit=1):
        SQL = "select messages.message_id, messages.filename from messages left join words on words.word_id=messages.message_id where words.word_id is Null and messages.inprogress_flag=FALSE" + " limit " + str(file_limit) + ";"
        return SQL


    @staticmethod
    def upsert_authors(author_ids, date):

        SQL = "insert into public.authors (author_id, author_name) VALUES\n"
        for author_id in author_ids:
            someauthor = author.get_by_id(author_id)
            SQL+="(\'" + str(author_id) + "\', \'" + queries.masking(someauthor.name) + "\'),\n"

        SQL = SQL[0:-2]
        SQL += " ON CONFLICT(author_id) DO NOTHING;"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def upsert_sources(source_ids, date):

        SQL = "insert into sources (source_id, source_name) VALUES\n"
        for source_id in source_ids:
            somesource = source.get_by_id(source_id)
            SQL += "(\'" + str(source_id) + "\', \'" + queries.masking(somesource.name) + "\'),\n"

        SQL = SQL[0:-2]
        SQL += " ON CONFLICT(source_id) DO NOTHING;"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def upsert_words(word_ids, date, table_name="words"):

        SQL = "insert into " + str(table_name) + " (word_id, text, creation_date) values "
        for someword_id in word_ids:
            someword = word.get_by_id(someword_id)
            SQL += "(\'" + str(someword.id) + "\', \'" + queries.masking(someword.unified_text)[0:256] + "\', \'" + str(date) + "\'), "

        SQL = SQL[0:-2]
        SQL += " ON CONFLICT(word_id) DO NOTHING;"

        logger.debug("SQL: " + str(SQL))
        return SQL


    @staticmethod
    def upsert_wordsinword(word_ids, table_name="wordsinword"):
        SQL = ""

        wordsinword_list = []
        for word_id in word_ids:
            someword = word.get_by_id(word_id)
            if someword.get_subwords():
                for subword_id, count in someword.get_subwords():
                    wordsinword_list.append([str(word_id), str(subword_id), str(count)])

        if len(wordsinword_list) > 0:
            SQL += "insert into " + table_name + " (mainword_id,subword_id,count) values "
            for record in wordsinword_list:
                SQL += "(\'" + record[0] + "\', \'" + record[1] + "\', \'" + record[2] + "\'), "

            SQL = SQL[0:-2]
            SQL += " ON CONFLICT (mainword_id,subword_id) DO NOTHING;"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def inprogress_messages(message_ids):
        SQL=""

        if len(message_ids) > 0:
            SQL += "update messages set inprogress_flag=True where message_id in ("

            for message_id in message_ids:
                SQL += "\'" + str(message_id) + "\', "

            SQL = SQL[0:-2]
            SQL += ");"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def upsert_messages(message_ids, date):

        SQL = "insert into messages (message_id, text, source_id, author_id, filename, creation_date) VALUES\n"
        for message_id in message_ids:
            somemessage = message.get_by_id(message_id)

            SQL += "(\'" + str(message_id) + "\', \'" + queries.masking(somemessage.unified_text)[0:256] + "\', \'" + str(somemessage.source_id) + "\', "
            SQL += "\'" + str(somemessage.author_id) + "\', \'" + str(somemessage.filename) + "\', \'"+ str(date) +"\'),\n"

        SQL = SQL[0:-2]
        SQL += " ON CONFLICT(message_id) DO UPDATE set inprogress_flag=FALSE;"

        logger.debug("SQL: " + str(SQL))
        return SQL

    @staticmethod
    def get_count_by_word_ids(word_ids):

        SQL = "SELECT sum(wordsinword.count) from wordsinword where mainword_id in ("

        for word_id in word_ids:
            SQL+='\''+str(word_id)+'\', '

        SQL=SQL[0:-2]
        SQL+=');'

        return SQL

    @staticmethod
    def delete_messages(message_ids):

        SQL = "delete from messages where message_id in ("
        for message_id in message_ids:
            SQL+="\'" + str(message_id) + "\', "

        SQL = SQL[0:-2]
        SQL += ");"

        logger.debug("SQL: " + str(SQL))
        return SQL

class db_parser:

    @staticmethod
    def force_utf8mb4(cursor):
        #was needed for MYSQL
        pass
        #cursor.execute('SET NAMES utf8mb4;')
        #cursor.execute("SET CHARACTER SET utf8mb4;")
        #cursor.execute("SET character_set_connection=utf8mb4;")

    @staticmethod
    def inprogress_messages(sql_session,msg_ids):
        logger.info("Setting Messages as in progress taken in work from pool")

        cursor = sql_session.cursor()
        cursor.execute(queries.inprogress_messages(msg_ids))
        sql_session.commit()
        cursor.close()

    @staticmethod
    def delete_messages(sql_session):
        logger.info("Deleting Messages taken in work from pool")

        cursor = sql_session.cursor()
        cursor.execute(queries.delete_messages(message.get_all_ids()))
        sql_session.commit()
        cursor.close()

    @staticmethod
    def get_new_words(sql_session,all_word_ids=word.get_all_ids()):
        new_word_ids = []

        cursor = sql_session.cursor()
        # iterator=cursor.execute(queries.get_new_words_ids_in_one_try(all_word_ids),multi=True)

        cursor.execute(queries.get_new_words_ids_create(all_word_ids))
        cursor.execute(queries.get_new_words_ids_select())

        for word_id_tuple in cursor:
            new_word_ids.append(word_id_tuple[0])

        cursor.close()

        logger.info("From total words: " + str(len(all_word_ids)) + " only "+ str(len(new_word_ids)) + " detected as new for db.")

        return new_word_ids

    @staticmethod
    def write_words_to_db(new_word_ids, sql_session, date, window=1024):
        logger.info("Starting writing words to DB")
        pointer = 0

        cursor = sql_session.cursor()

        while pointer < len(new_word_ids):
            logger.info("Current pointer: " + str(pointer) + " out of " + str(len(new_word_ids)) + " new words for DB.")
            word_ids = new_word_ids[pointer:pointer + window]

            try:
                SQL = queries.upsert_wordsinword(word_ids)

                if SQL != "":
                    cursor.execute(SQL)

                SQL = queries.upsert_words(word_ids, date)
                cursor.execute(SQL)
            except BaseException as exc:
                cursor.close()
                logger.error("SQL execution error: " + str(exc.__str__()) +" in write_word_to_db for SQL:" + str(SQL))
                raise Exception(str(exc.__str__()))

            sql_session.commit()

            pointer += window
            window += 128

        cursor.close()

    @staticmethod
    def sync_all_words_to_db(sql_session, date):

        logger.debug("Staring saving all new words to db")
        #db_parser.write_word_to_db(sorted_new_word_ids, sql_session, date)

        new_word_ids=db_parser.get_new_words(sql_session,word.get_all_ids())
        sorted_new_word_ids = word.get_ids_sorted_desc_by_subwords(new_word_ids)
        logger.debug("Staring saving all new words to db")
        db_parser.write_words_to_db(sorted_new_word_ids, sql_session, date)

    @staticmethod
    def check_save_consistency_words(sql_session):
        logger.info("Starting sync check for DB")
        WAIT_TIMER=60 #seconds

        logger.info("Collecting Local Statistics")
        app_subwords_count=0
        for someword in word.get_all():
            for subword_id,count in someword.get_subwords():
                app_subwords_count+=int(count)

        all_word_ids = word.get_all_ids()

        check_status=False
        while not check_status:

            db_subwords_count = -1

            cursor = sql_session.cursor()
            db_parser.force_utf8mb4(cursor)

            logger.info("Retrieving check counter from DB")
            cursor.execute(queries.get_count_by_word_ids(all_word_ids))

            for result in cursor:
                db_subwords_count=int(result[0])

            cursor.close()


            check_status=(db_subwords_count==app_subwords_count)

            if check_status:
                logger.info("Consistency check PASSED: db subwords=" + str(db_subwords_count) + " = app subowrds = " + str(app_subwords_count))
                return True

            else:
                logger.error("FAILED DB Consistency check: db subwords=" + str(db_subwords_count) + " and app subowrds = " + str(app_subwords_count))
                WAIT_TIMER+=random.randint(1,120)
                logger.error("Waiting for " + str(WAIT_TIMER) +" seconds - and rechecking again - possibly some other sessions have not finished!")

                time.sleep(WAIT_TIMER)


    @staticmethod
    def sync_all_authors_to_db(sql_session,date,temp_prefix=""):

        logger.info("Starting creating in DB Authors")
        cursor = sql_session.cursor()
        db_parser.force_utf8mb4(cursor)

        #for author_id in author.get_all_ids():
            #not needed in posgress
            #cursor.execute(queries.safe_author_create(author_id))
            #cursor.execute(queries.update_author(author_id, date))

        cursor.execute(queries.upsert_authors(author.get_all_ids(), date))
        sql_session.commit()

        cursor.close()

    @staticmethod
    def get_not_decomposed_messages(sql_session,file_limit=10):
        not_decomposed_list=[]

        logger.info("Starting lookup in DB for not decomposed messages")
        cursor = sql_session.cursor()
        db_parser.force_utf8mb4(cursor)
        cursor.execute(queries.get_not_decomposed_message_files(file_limit))

        for msg_id, somefile in cursor:
            not_decomposed_list.append([msg_id, somefile])

        logger.debug("All not decomposed files:" + str(not_decomposed_list))
        cursor.close()

        return not_decomposed_list

    @staticmethod
    def sync_all_sources_to_db(sql_session,date,temp_prefix=""):

        logger.info("Starting creating in DB Sources")
        cursor = sql_session.cursor()
        db_parser.force_utf8mb4(cursor)

        #for source_id in source.get_all_ids():
        #    cursor.execute(queries.safe_source_create(source_id))
        #    cursor.execute(queries.update_source(source_id, date))

        cursor.execute(queries.upsert_sources(source.get_all_ids(),date))

        sql_session.commit()

        cursor.close()

    @staticmethod
    def sync_all_messages_to_db(sql_session,date,temp_prefix=""):

        logger.info("Starting creating in DB messages")
        cursor = sql_session.cursor()
        db_parser.force_utf8mb4(cursor)

        #for message_id in message.get_by_id():
        #    cursor.execute(queries.safe_message_create(message_id))
        #    cursor.execute(queries.update_message(message_id, date))

        cursor.execute(queries.upsert_messages(message.get_by_id(), date))

        sql_session.commit()

        cursor.close()





class db:

    def __init__(self, **db_options):

        try:
            #self.sql_session = mysql.connector.connect(user=db_options.get('user'), password=db_options.get('password'), host=db_options.get('host'), port=db_options.get('port'), database=db_options.get('database'), use_unicode=True)
            self.sql_session = psycopg2.connect(user=db_options.get('user'), password=db_options.get('password'), host=db_options.get('host'), port=db_options.get('port'), database=db_options.get('database'))
            logger.info("Openning new DB connection")

        # except mysql.connector.Error as err:
        #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        #         logger.error("DB ERROR: Something is wrong with your user name or password")
        #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
        #         logger.error("DB ERROR: Database does not exist")


        except BaseException as err:
            logger.error("DB ERROR: Something is wrong in connecting to DB: " + str(err.__str__()))


    def get_new_word_ids(self):
        if len(word.get_all_ids()) > 0:
            return db_parser.get_new_words(self.sql_session)

    def sync_all_to_db(self):
        time_now = datetime.datetime.now()
        date = time_now.strftime('%Y-%m-%d %H:%M:%S')

        if len(author.get_all_ids()) > 0:
            db_parser.sync_all_authors_to_db(self.sql_session,date)

        if len(source.get_all_ids()) > 0:
            db_parser.sync_all_sources_to_db(self.sql_session,date)

        if len(word.get_all_ids()) > 0:
            db_parser.sync_all_words_to_db(self.sql_session,date)

        if len(message.get_all_ids()) > 0:
            db_parser.sync_all_messages_to_db(self.sql_session,date)

    def remove_messages_from_db(self):
        if len(message.get_all_ids()) > 0:
            db_parser.delete_messages(self.sql_session)

    def inprogress_messages(self, msg_ids):
        if len(msg_ids) > 0:
            db_parser.inprogress_messages(self.sql_session,msg_ids)

    def check_sync(self):
        if len(word.get_all_ids()) > 0:
            db_parser.check_save_consistency_words(self.sql_session)


    def get_not_decomposed_messages(self,file_limit=10):
        return db_parser.get_not_decomposed_messages(self.sql_session,file_limit)


    def close_db(self):
        self.sql_session.close()
        logger.info("DB connection closed")
