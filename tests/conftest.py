"""pytest entry.
"""

import pytest

from bh_aust_postcode import create_app

from bh_aust_postcode.api.postcode_pool import (
    PostcodePool,
    postcode_pool,
    load_postcode,
)

from tests import database_filename

@pytest.fixture(scope='module')
def app():
    app = create_app()

    app.app_context().push()

    return app

@pytest.fixture(scope='module')
def test_client(app):
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def ensure_postcodes_loaded(app):
    """Will-nilly load postcodes for test methods. 
    Postcodes loaded only once during application / test lifetime.
    """
    
    load_postcode(database_filename(app))
    assert postcode_pool.count >= 18000
