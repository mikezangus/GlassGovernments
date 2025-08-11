def normalize_space(input: str | None) -> str | None:
    if not input:
        return None
    output = " ".join(input.split())
    return output if output else None
