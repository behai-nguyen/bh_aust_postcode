"""Test Business rules ( logic ).

Note on ensure_postcodes_loaded() fixure: 

It is to ensure the singleton instance bh_aust_postcode.api.postcode_pool.postcode_pool
loads postcodes for testing.

It gets called repeatedly for each test method, however, the loading only carried out
only once.
"""

from http import HTTPStatus

import pytest

from bh_aust_postcode.api.bro import search_by_locality

from tests import search_postcode

@pytest.mark.bro
def test_bro_search_by_locality_valid(ensure_postcodes_loaded):
    """Search which returns some localities.
    """

    status = search_by_locality('spring')

    assert status['status']['code'] == HTTPStatus.OK.value

    assert ('data' in status) == True
    assert ('localities' in status['data']) == True

    localities = status['data']['localities']
    assert len(localities) > 1

    found = search_postcode(localities, 'TAMBAR SPRINGS', 'NSW', '2381')
    assert found == True

    found = search_postcode(localities, 'SPRINGLANDS', 'QLD', '4804')
    assert found == True

@pytest.mark.bro
def test_bro_search_by_locality_not_found(ensure_postcodes_loaded):
    """Search which returns nothing.
    """

    status = search_by_locality('xyz')

    assert status['status']['code'] == HTTPStatus.NOT_FOUND.value

@pytest.mark.bro
def test_bro_search_by_locality_invalid_01(ensure_postcodes_loaded):
    """Search where locality / suburb to search for less than minimum length.
    """

    status = search_by_locality('Sp')

    assert status['status']['code'] == HTTPStatus.BAD_REQUEST.value

@pytest.mark.bro
def test_bro_search_by_locality_invalid_02(ensure_postcodes_loaded):
    """Search where locality / suburb to search for contains invalid characters.
    """

    status = search_by_locality('%^& Spring')

    assert status['status']['code'] == HTTPStatus.BAD_REQUEST.value
        