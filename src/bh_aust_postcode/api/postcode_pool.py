"""
Implement a singleton class which holds all Australian postcodes and a locality / suburb 
search method.

    Reference:
        https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python#answer-6581949
        What are metaclasses in Python?

Relevant test modules:

    * ./tests/test_postcode_pool.py
"""

import logging

import psycopg2

from flask import current_app as app

from src.bh_aust_postcode.utils import (
    print_log,
    format_sql_statement,
)
from src.bh_aust_postcode.config import get_database_connection

logger = logging.getLogger('admin')

class PostcodePoolMeta(type):
    """Singleton pattern metaclass."""
    singletons = {}

    def __call__(cls, *args, **kwargs):
        if cls in PostcodePoolMeta.singletons:
            # We return the only instance and skip a call to __new__() and __init__()...
            return PostcodePoolMeta.singletons[cls]

        # ...else if the singleton isn't present we proceed as usual.
        instance = super(PostcodePoolMeta, cls).__call__(*args, **kwargs)
        PostcodePoolMeta.singletons[cls] = instance
        return instance

class PostcodePool(object, metaclass=PostcodePoolMeta):
    """Hold all Australian postcodes and provide a locality / suburb search method. 

    Class attributes:
        | postcodes = []. List of postcodes. Each postcode dictionary has the following 
            text fields: ``locality``, ``state`` and ``postcode``.
    """    

    #: Class attribute. List of postcodes. Each postcode dictionary has the following text fields: ``locality``, ``state`` and ``postcode``.
    postcodes = []

    def __entity_exists(self, connection: object, sql_statement: str) -> bool:
        """Check if a PostgreSQL database schema or table exists.

        :param object connection: an already established PostgreSQL connection.
        :param sql_statement str: the complete SQL entity selection.

        :return: a Boolean value which indicates whether an entity exists.
        :rtype: bool.
        """
        try:
            cursor = connection.cursor()
            cursor.execute(sql_statement)
            exists = cursor.fetchone()[0]
        finally:
            cursor.close()
            return exists
        
    def __schema_exists(self, connection: object) -> bool:
        """Check if the database has a schema whose name matches configured schema name.

        :param object connection: an already established PostgreSQL connection.

        :return: a Boolean value which indicates if the schema exists.
        :rtype: bool.
        """

        sql = "SELECT EXISTS(SELECT 1 FROM pg_namespace WHERE nspname = '{0}')"
        return self.__entity_exists(connection, format_sql_statement(sql))
    
    def __table_exists(self, connection: object) -> bool:
        """Check if the database and schema has a table whose name matches configured 
        table name.

        :param object connection: an already established PostgreSQL connection.

        :return: a Boolean value which indicates if the table exists.
        :rtype: bool.
        """

        sql = ("SELECT EXISTS( "
                "SELECT 1 FROM information_schema.tables "
                "WHERE table_schema = '{0}' AND table_name = '{1}')")
        return self.__entity_exists(connection, format_sql_statement(sql))
    
    def __get_database_info(self) -> tuple:
        return app.config['SCHEMA_NAME'], app.config['POSTCODE_TABLE_NAME']

    def load(self, force_reload=False) -> tuple:
        """Load all postcodes from the database into :attr:`~.PostcodePool.postcodes`.

        :param bool force_reload: force reloading postcodes the database.

        :return: a Boolean result and a possible error message. 
        :rtype: tuple.
        """
        try:
            db_conn_params = get_database_connection()            
            connection = psycopg2.connect(**db_conn_params)

            result = False
            message = ''

            schema_name, postcode_table_name = self.__get_database_info()

            if (not self.__schema_exists(connection)):
                message = "Database schema {!r} does not yet exist.".format(schema_name)
                print_log(logger, message, 'info')
                return
            
            if (not self.__table_exists(connection)):
                message = "Database table {!r} does not yet exist.".format(postcode_table_name)
                print_log(logger, message, 'info')
                return

            result = True

            if force_reload:
                logger.info('Force reloading.')
                PostcodePool.postcodes.clear()
            else:
                if len(PostcodePool.postcodes) > 0:
                    logger.info('Postcodes have already been loaded.')
                    return

            cursor = connection.cursor()

            cursor.execute(format_sql_statement('SELECT * FROM {0}.{1} ORDER BY locality, state, postcode'))
            for row in cursor:
                postcode = {'locality': row[1], 'state': row[2], 'postcode': row[3]}
                PostcodePool.postcodes.append(postcode)
            cursor.close()

            logger.info(f'Loaded {len(PostcodePool.postcodes)} postcodes into pool.')

        except Exception as error:
            result = False
            message = str(error)
            logger.exception(message)

        finally:
            if connection:
                connection.close()
            return result, message

    def search(self, locality: str) -> list:
        """Match postcodes based on locality / suburb. It is a partial match.

        :param str locality: the locality / suburb to match on. It always assumes this 
            is a partial name of a locality / suburb. The match is always partial.

        :return: a list matching postcode(s). Each postcode has the following text fields
            : ``locality``, ``state`` and ``postcode``.
        :rtype: tuple.
        """
        result = [pc for pc in PostcodePool.postcodes 
                    if locality.upper() in pc['locality'].upper()]
        
        return result

    @property
    def count(self) -> str: 
        """Read only property. Total number of postcodes in :attr:`~.PostcodePool.postcodes`.
        """
        return len(PostcodePool.postcodes)
    
### TO_DO:
    
postcode_pool = PostcodePool()

def load_postcode():
    postcode_pool.load()