import json
import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_fips_to_state() -> dict:
    with open(os.path.join(
        CURRENT_DIR,
        "fips_to_state.json"
    ), "r") as file:
        return json.load(file)
