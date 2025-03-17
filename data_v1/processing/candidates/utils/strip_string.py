import re


def strip_string(input: str) -> str:
    return re.sub(
        pattern = r'\s*\([^)]*\)',
        repl = "",
        string = input
    )
