import re


def flatten_text(text: str) -> str:
    flattened_lines = []
    for line in text.splitlines():
        line = line.strip()
        line = re.sub(r'^\d+\s+', '', line)
        if not line or re.fullmatch(r'\*+', line):
            continue
        flattened_lines.append(line)
    return ' '.join(flattened_lines)
