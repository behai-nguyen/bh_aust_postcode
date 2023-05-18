"""Test PostcodePool singleton.

Note on ensure_postcodes_loaded() fixure: 

It is to ensure the singleton instance bh_aust_postcode.api.postcode_pool.postcode_pool
loads postcodes for testing.

It gets called repeatedly for each test method, however, the loading only carried out
only once.
"""

import pytest

from bh_aust_postcode.api.postcode_pool import (
    PostcodePool,
    postcode_pool,
)

from tests import search_postcode

@pytest.mark.postcode_pool
def test_postcode_pool_singleton(ensure_postcodes_loaded, app):
    """Test PostcodePool singleton behaviour.
    """

    assert postcode_pool != None

    postcode_pool_2 = PostcodePool()

    # Singleton.
    assert (postcode_pool_2 is postcode_pool) == True

    assert postcode_pool.count >= 18000

@pytest.mark.postcode_pool
def test_postcode_pool_search(ensure_postcodes_loaded, app):
    """Test PostcodePool search method.
    """

    assert postcode_pool != None
    assert postcode_pool.count >= 18000

    result = postcode_pool.search('springva')

    assert len(result) > 1

    found = search_postcode(result, 'SPRINGVALE', 'VIC', '3171')
    assert found == True
