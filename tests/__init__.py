"""
Tests helper functions.
"""

import os

def database_filename(app):
    return os.path.join(app.instance_path, '', app.config['DATABASE'])

def search_postcode(list: list, locality: str, state: str, postcode: str) -> bool:
    found = False
    for pc in list:
        if (pc['locality'] == locality.upper() and pc['state'] == state.upper()
            and pc['postcode'] == postcode.upper()):
            found = True
            break

    return found    