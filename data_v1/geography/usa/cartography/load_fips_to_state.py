import json
import os


def load_fips_to_state() -> dict:
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "fips_to_state.json"
        ),
        "r"
    ) as f:
        return json.load(f)
