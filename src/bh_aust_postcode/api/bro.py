"""Business rules ( logic ) for /aust-postcode API endpoints.

Relevant test modules:

    * ./tests/test_bro.py
"""

import re

from http import HTTPStatus

from bh_apistatus.result_status import make_status

from bh_aust_postcode.api.postcode_pool import postcode_pool

MIN_LOCALITY_LENGTH = 3

INFO_INVALID_TOO_SHORT_MSG = "Must have at least {!r} characters: {!r}"
INFO_INVALID_CHARACTERS_MSG = ("{!r} is invalid. Accept only letters, space, hyphen and "
                               "single quote characters." )
INFO_NO_MATCHED_MSG = 'No localities matched {!r}'

def search_by_locality(locality: str) -> dict:
    """Partial search postcodes based on locality and return matched localities
    wrapped in a dictionary.

    :param str locality: the locality / suburb to match on. It always assumes this 
        is a partial name of a locality / suburb. The match is always partial.

    :return: dictionary representation of 
        `ResultStatus <https://bh-apistatus.readthedocs.io/en/latest/result-status.html>`_.

    Further illustrations of return value, as a dictionary.

    On successful::
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

    Nothing found::
        {
            "status": {
                "code": 404,
                "text": "No localities matched 'xyz'"
            }
        }

    Invalid searches::
        {
            "status": {
                "code": 400,
                "text": "'%^& Spring' is invalid. Accept only letters, space, hyphen and single quote characters."
            }
        }

        {
            "status": {
                "code": 400,
                "text": "Must have at least 3 characters: 'Sp'"
            }
        }

    In general ['status']['code'] other than HTTPStatus.OK.value signifies search does not
    return any localities. Always check for ['status']['code'] of HTTPStatus.OK.value before
    proceeding any further with the result.
    """

    if (len(locality) < MIN_LOCALITY_LENGTH):
        return make_status(HTTPStatus.BAD_REQUEST, 
                           INFO_INVALID_TOO_SHORT_MSG.format(MIN_LOCALITY_LENGTH, locality)).as_dict()

    # Locality / suburb contains only letters, space, - and '.
    if not re.compile(r"^[A-Za-z, ' ', -, ']+$").match(locality):
        return make_status(HTTPStatus.BAD_REQUEST, 
                           INFO_INVALID_CHARACTERS_MSG.format(locality)).as_dict()
            
    localities = postcode_pool.search(locality)

    if len(localities) > 0: return make_status().add_data(localities, 'localities').as_dict()

    return make_status(HTTPStatus.NOT_FOUND, INFO_NO_MATCHED_MSG.format(locality)).as_dict()