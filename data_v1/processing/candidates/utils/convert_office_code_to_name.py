def convert_office_code_to_name(chamber_code: str) -> str:
    offices__dict = {
        "H": "Congress",
        "S": "Senate"
    }
    return offices__dict.get(chamber_code, "")
