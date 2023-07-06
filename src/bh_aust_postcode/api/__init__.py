""" Flask-RESTX API blueprint configuration. """

from flask import Blueprint
from flask_restx import Api

from src.bh_aust_postcode.api.routes import tree_ns

api_bp = Blueprint( 'api', __name__, url_prefix='/api/v0' )

api = Api(
    api_bp,
    version='1.0',
    title='Australian Postcode API',
    description='Welcome to Australian Postcode API with Swagger UI documentation',
    doc='/ui',
)

api.add_namespace( tree_ns, path='/aust-postcode' )
