"""Flask Application entry point."""

from src.bh_aust_postcode import create_app
from src.bh_aust_postcode.api.postcode_pool import load_postcode

app = create_app()

with app.app_context():
    load_postcode()
    from bh_aust_postcode.commands import update_postcode
