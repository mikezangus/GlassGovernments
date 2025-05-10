from fetch_updates import fetch_updates
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(STATE_DIR))
PIPELINES_DIR = os.path.dirname(STATE_DIR)
sys.path.append(os.path.dirname(PIPELINES_DIR))
from insert_to_db import insert_to_db


updates = fetch_updates()
insert_to_db("bill_actions", updates)