import mysql.connector
import re
import datetime

from mysql.connector import errorcode

import logging.config


logger = logging.getLogger('db')

class queries:

    @staticmethod
    def to_null(element):
        if element == '' or element == 0 or element is None:
            return 'null'
        else:
            return "\'" + str(element) + "\'"

    @staticmethod
    def sql_injection_protection(element):
        key_words=['select','drop','insert','delete','describe']

        for word in key_words:
            if word.upper() in element.upper:
                logger.warning("SQL Injection detected in input %s" % (element))

                insensitive_replace= re.compile(re.escape(word), re.IGNORECASE)
                element = insensitive_replace.sub('',element)

        return element


class db_parser:
    @staticmethod
    def force_utf8mb4(cursor):
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute("SET CHARACTER SET utf8mb4")
        cursor.execute("SET character_set_connection=utf8mb4")



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


    def load_orders_from_db(self):
        db_parser.create_orders(self.sql_session)

    def sync_user_to_db(self, user_id):
        db_parser.safe_user_to_db(self.sql_session, user_id)

    def sync_cart_to_db(self, chat_id):
        db_parser.safe_cart_create(self.sql_session, chat_id)
        db_parser.sync_cart_to_db(self.sql_session, chat_id)
        db_parser.update_cart_products_to_db(self.sql_session, chat_id)

        cart.set_synced_to_db(chat_id)

    def sync_chat_to_db(self, chat_id):
        db_parser.safe_cart_create(self.sql_session, chat_id)
        db_parser.update_chat_last_menu_msg_to_db(self.sql_session, chat_id)


    def sync_order_to_db(self, order_id):
        db_parser.safe_order_to_db(self.sql_session, order_id)
        db_parser.update_products_in_order_to_db(self.sql_session, order_id)

    def sync_tracked_response_to_db(self, response):
        db_parser.safe_tracked_response_to_db(self.sql_session, response)

    def sync_chat_tracked_responses_to_db(self, chat_id):
        db_parser.safe_chat_tracked_responses_to_db(self.sql_session, chat_id)

    def load_chats_from_db(self):
        db_parser.create_chats(self.sql_session)

    def load_tracked_response(self,limit=1000):
        db_parser.load_tracked_response(self.sql_session,limit)

    def load_some_orders_from_db(self, chat_id=None, order_id=None):
        db_parser.recreate_orders(self.sql_session, chat_id, order_id)

    def load_some_users_from_db(self,user_id=None):
        db_parser.recreate_users(self.sql_session,user_id)

    def load_some_carts_from_db(self,chat_id=None):
        db_parser.recreate_carts(self.sql_session,chat_id)

    def load_products_from_db(self):
        db_parser.create_products(self.sql_session)
        db_parser.create_productgroups(self.sql_session)

    def sync_notifications_to_db(self, notification_obj):
        db_parser.sync_notifications_to_db(self.sql_session, notification_obj)

    def load_all_from_db(self):
        db_parser.create_users(self.sql_session)
        db_parser.create_products(self.sql_session)
        db_parser.create_productgroups(self.sql_session)

        db_parser.create_carts(self.sql_session)
        db_parser.create_orders(self.sql_session)
        #orders are parsed from DB to keep order_id uniquenesss

        db_parser.create_discounts(self.sql_session)

        db_parser.create_stickers(self.sql_session)
        db_parser.create_chats(self.sql_session)

    def sync_all_to_db(self):
        for user_id in user.list_users.keys():
            self.sync_user_to_db(user_id)

        for chat_id in cart.list_chats.keys():
            self.sync_cart_to_db(chat_id)

        for order_id in order.list_orders.keys():
            self.sync_cart_to_db(order_id)

    def log(self,msg):
        db_parser.create_log_record(self.sql_session,msg)
        pass

    def close_db(self):
        self.sql_session.close()
        logger.info("DB connection closed")