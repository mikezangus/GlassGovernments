import re


regex_split_text_and_nums = r"([a-zA-Z]+)(\d+)"


committee_regex = re.compile(
    r'(?:\d{1,2}/\d{1,2}/\d{4}\s*)?'
    r'(?:re-)?(?:referred to|reported as (?:committed|amended) (?:from|by)|re-?committed to|committed to)'
    r'\s+([^\[\]]+?)\s+\[(House|Senate)\]',
    re.IGNORECASE
)
