def normalize_null(value: str | None, default: str | None = None) -> str | None:
    if value is None:
        return default
    normalized = " ".join(value.split())
    return normalized if normalized else default
