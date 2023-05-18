"""Test end points.

Test end points currently implemented, e.g.:
    http://localhost:5000/api/v0/aust-postcode/{locality}

Note on ensure_postcodes_loaded() fixure: 

It is to ensure the singleton instance bh_aust_postcode.api.postcode_pool.postcode_pool
loads postcodes for testing.

It gets called repeatedly for each test method, however, the loading only carried out
only once.
"""
from http import HTTPStatus
import pytest
import simplejson as json

from tests import search_postcode

@pytest.mark.api_endpoints
def test_locality_search_endpoints(ensure_postcodes_loaded, app, test_client):
    """Test end point such as 
    http://localhost:5000/api/v0/aust-postcode/spring
    """

    response = test_client.get('/api/v0/aust-postcode/spring')

    assert response != None
    assert response.status_code == HTTPStatus.OK.value

    status = json.loads(response.get_data(as_text=True))

    assert status['status']['code'] == HTTPStatus.OK.value

    assert ('data' in status) == True
    assert ('localities' in status['data']) == True

    localities = status['data']['localities']
    assert len(localities) > 1

    found = search_postcode(localities, 'SPRINGVALE', 'VIC', '3171')
    assert found == True
