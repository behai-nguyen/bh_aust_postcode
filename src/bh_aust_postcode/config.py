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
    SECRET_KEY = environ.get( 'SECRET_KEY' )
    FLASK_APP = environ.get( 'FLASK_APP' )
    FLASK_DEBUG = strtobool( environ.get('FLASK_DEBUG') )

    SOURCE_POSTCODE_URL = environ.get( 'SOURCE_POSTCODE_URL' )
    SCHEMA = environ.get( 'SCHEMA' )
    DATABASE = environ.get( 'DATABASE' )

def get_config():
    """Retrieve environment configuration settings."""
    return Config