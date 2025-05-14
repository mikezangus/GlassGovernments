from datetime import datetime, timezone
from convert_guid_to_id import convert_guid_to_id


def parse_actions(entry: dict[str, any]) -> dict[str, any]:
    return {
        "id": convert_guid_to_id("PA", entry["id"]),
        "last_action": entry["parss_lastaction"].split(',')[0],
        "enacted": entry["parss_enacted"].upper() == "YES",
        "passed_lower": entry["parss_passedhouse"].upper() == "YES",
        "passed_upper": entry["parss_passedsenate"].upper() == "YES",
        "pubdate": datetime(
            *entry["published_parsed"][:6],
            tzinfo=timezone.utc
        ).isoformat(),
        "prime_sponsor": ' '.join((entry["parss_primesponsor"].split(' ')[1:])),
        "cosponsors": entry["parss_cosponsors"] \
            .replace(" and ", ", ") \
            .replace(", ", ',') \
            .split(',')
    }
