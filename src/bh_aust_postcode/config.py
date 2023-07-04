"""
Flask configuration variables.
"""
from os import (
    getcwd, 
    environ, 
    path,
)

from dotenv import load_dotenv

from distutils.util import strtobool

basedir = getcwd()
load_dotenv( path.join(basedir, '.env') )

class Config:
    """Set Flask configuration from .env file."""

    # General Config.
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_DEBUG = strtobool(environ.get('FLASK_DEBUG'))

    #: The URL of the source postcodes in JSON format.
    SOURCE_POSTCODE_URL = environ.get('SOURCE_POSTCODE_URL')
    #: Whether or not to keep a copy of the downloaded postcodes.
    KEEP_DOWNLOADED_POSTCODES = strtobool(environ.get('KEEP_DOWNLOADED_POSTCODES'))

    #: PostgreSQL database creation script: create schema and table.
    DB_CREATE_SCRIPT = environ.get('DB_CREATE_SCRIPT')

    #: The PostgreSQL schema name.
    SCHEMA_NAME = environ.get('SCHEMA_NAME')
    #: The PostgreSQL table name.
    POSTCODE_TABLE_NAME = environ.get('POSTCODE_TABLE_NAME')

    #: PostgreSQL host name.
    HOST = environ.get('HOST')
    #: PostgreSQL database. This database must exist on host.
    DATABASE = environ.get('DATABASE')
    #: PostgreSQL user. This is the PostgreSQL user who has access to database.
    PG_USER = environ.get('PG_USER')
    #: PostgreSQL password. This is password to log into the PostgreSQL.
    PASSWORD = environ.get('PASSWORD')
    #: PostgreSQL port. The PostgreSQL host port.
    PORT = environ.get('PORT')

def get_config():
    """Retrieve environment configuration settings.

    :return: object.
    :rtype: :class:`Config`.
    """
    return Config

def get_database_connection():
    """Construct a dictionary suitable to connect to the target PostgreSQL 
    database using psycopg2.

    :return: a dictionary represents psycopg2 connection parameters.
    :rtype: dict.
    """
    cfg = get_config()

    return {
        'host': cfg.HOST,
        'database': cfg.DATABASE,
        'user': cfg.PG_USER,
        'password': cfg.PASSWORD,
        'port': cfg.PORT,
    }
