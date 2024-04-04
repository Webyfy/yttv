from os import path
from typing import Union

BIN_DIRECTORY = path.dirname(path.realpath(__file__))

def get_icon_path(icon_name)->Union[str, None]:
    if icon_name is None:
        return None
    icon_location = path.join(
        BIN_DIRECTORY, 'icons', icon_name)
    if not path.isfile(icon_location):
        # Resource not found
        icon_location = None

    return icon_location
