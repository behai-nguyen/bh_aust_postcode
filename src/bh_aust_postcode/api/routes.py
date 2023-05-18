"""API endpoint definitions for /trees namespace.

Relevant test modules:

    * ./tests/test_api_endpoints.py
    * ./tests/test_bro.py
"""

from http import HTTPStatus

from flask_restx import Namespace, Resource

from bh_aust_postcode.api.bro import search_by_locality

tree_ns = Namespace( name="postcodes", validate=True )

@tree_ns.route('/<locality>')
@tree_ns.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
@tree_ns.response(int(HTTPStatus.NOT_FOUND), 'No matching localities.')
@tree_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
@tree_ns.param('locality', 'The locality search text')
class Postcode(Resource):
    """ Handles HTTP requests to URL: /postcodes. """

    @tree_ns.response(int(HTTPStatus.OK), 'Matched localities.')
    def get(self, locality):
        """Search postcodes based on locality. 

        Param locality is assumed to be partial. The search is based on partial matching.
        
        Return matched localities wrapped in a dictionary.

        On successful:

            {
                "status": {
                    "code": 200,
                    "text": ""
                },
                "data": {
                    "localities": [
                        {
                            "locality": "ALICE SPRINGS",
                            "state": "NT",
                            "postcode": "0870"
                        },
                        ...
                    {
                            "locality": "WILLOW SPRINGS",
                            "state": "SA",
                            "postcode": "5434"
                        }
                    ]
                }
            }

        Nothing found:

            {
                "status": {
                    "code": 404,
                    "text": "No localities matched 'xyz'"
                }
            }

            {
                "status": {
                    "code": 400,
                    "text": "'%^& Spring' is invalid. Accept only letters, space, hyphen and single quote characters."
                }
            }

        Invalid searches:

            {
                "status": {
                    "code": 400,
                    "text": "Must have at least 3 characters: 'Sp'"
                }
            }

        In general ``['status']['code']`` other than ``HTTPStatus.OK.value`` signifies search does \
            not return any localities. Always check for ``['status']['code']`` of ``HTTPStatus.OK.value`` \
            before proceeding any further with the result.
        """
        
        return search_by_locality(locality)