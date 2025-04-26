import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from fetch_from_db import fetch_from_db


def fetch_bill_metadata() -> list:
    return fetch_from_db("pa_bill_metadata", { "select": '*' })
