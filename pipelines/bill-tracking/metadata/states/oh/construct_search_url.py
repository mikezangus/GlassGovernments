from urllib.parse import quote
from metadata.states.oh.enums import LegislationType


def construct_search_url(
    session: int,
    page_start: int,
    page_size: int,
    legislation_types: list[LegislationType]
) -> str:
    if not legislation_types:
        return ""
    legislation_types_str = ",".join(quote(type.value) for type in legislation_types)
    params = {
        "generalAssembly": session,
        "start": page_start,
        "pageSize": page_size,
        "sort": "Number",
        "extendedLegislationTypes": legislation_types_str
    }
    params_str = "&".join(f"{key}={value}" for key, value in params.items())
    return f"https://legislature.ohio.gov/legislation/search?{params_str}"
