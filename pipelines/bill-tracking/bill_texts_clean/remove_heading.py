def remove_heading(text: str) -> str:
    lines = text.splitlines()
    start_idx = None
    for i, line in enumerate(lines):
        line = line.strip().upper()
        if line.startswith("A ") or line.startswith("AN "):
            start_idx = i + 1
            break
    return "\n".join(lines[start_idx:]) \
        if start_idx is not None \
        else text
