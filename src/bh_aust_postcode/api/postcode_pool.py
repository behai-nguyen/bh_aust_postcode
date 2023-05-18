"""
Implement a singleton class which holds all Australian postcodes and a locality / suburb 
search method.

    Reference:
        https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python#answer-6581949
        What are metaclasses in Python?

Relevant test modules:

    * ./tests/test_postcode_pool.py
"""

import os
import logging

import sqlite3

from bh_aust_postcode.utils import print_log

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

    def load(self, database_file: str, force_reload=False) -> tuple:
        """Load all postcodes from the instance SQLite database file into :attr:`~.PostcodePool.postcodes`.

        :param str database_file: absolute location of the instance SQLite database file.
        :param bool force_reload: force reloading postcodes from the instance SQLite database file.

        :return: a Boolean result and a possible error message. 
        :rtype: tuple.
        """

        if (not os.path.exists(database_file)):
            msg = "Database file {!r} does not yet exist.".format(database_file)
            print_log(logger, msg, 'info')
            return False, msg

        if force_reload:
            logger.info('Force reloading.')
            PostcodePool.postcodes.clear()
        else:
            if len(PostcodePool.postcodes) > 0:
                logger.info('Postcodes have already been loaded.')
                return True, ''

        try:
            result = True
            error_message = ''

            sqliteConnection = sqlite3.connect(database_file)
            cursor = sqliteConnection.cursor()

            cursor.execute('SELECT * FROM postcode ORDER BY locality, state, postcode')
            for row in cursor:
                postcode = {'locality': row[1], 'state': row[2], 'postcode': row[3]}
                PostcodePool.postcodes.append(postcode)
            cursor.close()

        except sqlite3.Error as error:
            result = False
            error_message = str(error)
            logger.exception(error_message)

        finally:
            if sqliteConnection:
                sqliteConnection.close()
            return result, error_message

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

def load_postcode(database_file: str):
    postcode_pool.load(database_file)