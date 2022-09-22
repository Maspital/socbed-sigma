#!/usr/bin/env python3

from datetime import datetime
from time import time


def print_with_timestamp(text):
    print(f"\033[1m{get_iso_time()}:\033[0m {text}")


def get_iso_time(time_in_seconds=None):
    if time_in_seconds:
        return datetime.utcfromtimestamp(time_in_seconds).isoformat() + "Z"
    else:
        return datetime.utcnow().isoformat() + "Z"


def get_epoch():
    return int(time())
