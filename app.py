"""Flask Application entry point."""

import os

from bh_aust_postcode import create_app
from bh_aust_postcode.api.postcode_pool import load_postcode

app = create_app()

sqlite_database_file = os.path.join(app.instance_path, '', app.config['DATABASE'])
load_postcode(sqlite_database_file)

with app.app_context():
    from bh_aust_postcode.commands import update_postcode
