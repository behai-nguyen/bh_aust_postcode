"""Flask app initialization via factory pattern."""

import os

from flask import Flask
from flask_cors import CORS

import yaml
import logging
import logging.config

from bh_aust_postcode.config import get_config

cors = CORS()

def create_app(config=None):
    app = Flask('bh-aust-postcode', instance_relative_config=True)

    app.config.from_object(config if config != None else get_config())

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_loggers()

    from bh_aust_postcode.api import api_bp
    app.register_blueprint(api_bp)
	
    cors.init_app(app)
    
    return app

def register_loggers():
    with open('omphalos-logging.yml', 'rt') as file:
        config = yaml.safe_load(file.read())
        logging.config.dictConfig(config)
