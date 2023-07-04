"""
Download postcodes JSON source, extract locality, state, postcode to write
to local SQLite database file. Downloaded JSON source also gets written to
a local JSON file.
"""

from datetime import datetime
import os
import logging
import requests
import traceback
import sys
import psycopg2

from flask import current_app as app

from bh_utils.json_funcs import dumps

from bh_aust_postcode.config import get_database_connection
from bh_aust_postcode.utils import (
    print_log,
    format_sql_statement,
)

logger = logging.getLogger('admin')

def __schema_filename():
    """Get SQLite scheme file name to create the database file name.

    :return: full path of PostgreSQL database creation script: create schema and table.
    :rtype: str.
    """

    return os.path.join(os.path.dirname(__file__), '', app.config['DB_CREATE_SCRIPT'])

def create_database():
    """Creates a new SQLite database file, overwrites any existing one."""
    try:
        db_conn_params = get_database_connection()
        
        connection = psycopg2.connect(**db_conn_params)
        cursor = connection.cursor()

        with open(__schema_filename(), 'r') as sqlite_file:
            sql_script = sqlite_file.read()

        cursor.execute(format_sql_statement(sql_script))
        cursor.close()

        connection.commit()

    except Exception as e:
        print_log(logger, 'Error creating database file {!r}.'.format(e), 'exception')

    finally:
        if connection:
            connection.close()

def get_json_content() -> tuple:
    """Download postcodes JSON source.

    :return: True, JSON data. False, error message.
    :rtype: tuple.
    """
    try:
        response = requests.get(app.config['SOURCE_POSTCODE_URL'])
        response.raise_for_status()

    except Exception as e:
        msg = "Error getting JSON source {!r}.".format(e)
        print_log(logger, msg, 'exception')
        return False, msg
    
    return True, response.json()

def write_downloaded_json_content(json: dict) -> None:
    """Conditionally write downloaded postcode JSON content to a JSON 
    file on disk.

    If environment variable KEEP_DOWNLOADED_POSTCODES is True, then
    write the downloaded source postcodes to disk. 

    :param JSON json: downloaded postcodes to write to a local JSON file.    
    """
    if (not app.config['KEEP_DOWNLOADED_POSTCODES']):
        return
    
    local_dt_str = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S_%f")[:-3]
    file_name = os.path.join(app.instance_path, '', f"australian_postcodes_{local_dt_str}.json")

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write( dumps(json) )
        f.close()

    print_log(logger, "Downloaded JSON: {!r}".format(file_name), 'info')

def extract_and_insert():
    """Download postcodes JSON source, write JSON source to local file,
    then read locality, state and postcode from JSON data and write to 
    SQLite database file. 
    """

    try:
        db_conn_params = get_database_connection()
        connection = psycopg2.connect(**db_conn_params)
        cursor = connection.cursor()

        res, data = get_json_content()

        if (not res): 
            print_log(logger, "Error getting source JSON postcode data: {!r}".format(data), 'error')
            return
        
        json_obj = data

        print_log(logger, f"Total postcodes read: {len(json_obj)}", 'info')

        write_downloaded_json_content(json_obj)

        #
        # raise Exception("This is a test only...")
        #

        total_inserted = 0

        for itm in json_obj:
            locality = itm['locality'].replace("'", "''")
            state = itm['state']
            postcode = itm['postcode']

            insert_query = ("INSERT INTO {0}.{1} (locality, state, postcode)  "
                            f"VALUES ('{locality}', '{state}', '{postcode}')")

            cursor.execute(format_sql_statement(insert_query))
            total_inserted += 1

        connection.commit()
        cursor.close()

        print_log(logger, f"Total postcodes inserted into database: {total_inserted}.", 'info')

    except Exception as e:
        print_log(logger, 'Error inserting {!r}'.format(e), 'exception')
        print_log(logger, 'Exception traceback:', 'exception')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print_log(logger, traceback.format_exception(exc_type, exc_value, exc_tb), 'exception')
    finally:
        if connection:
            connection.close()

# Command.

@app.cli.command('update-postcode', short_help='Download and update postocdes.')
def update_postcode():
    """Download and update postocdes."""

    create_database()
    extract_and_insert()
