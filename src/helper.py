#!/usr/bin/env python3

from datetime import datetime
from time import time
from pathlib import Path


def print_with_timestamp(text):
    print(f"\033[1m{get_iso_time()}:\033[0m {text}")


def get_iso_time(time_in_seconds=None):
    if time_in_seconds:
        return datetime.utcfromtimestamp(time_in_seconds).isoformat() + "Z"
    else:
        return datetime.utcnow().isoformat() + "Z"


def get_epoch():
    return int(time())


def extend_filename(original_name, new_suffix):
    path = Path(original_name)
    return "{0}_{2}{1}".format(Path.joinpath(path.parent, path.stem),
                               path.suffix,
                               new_suffix)
