import requests
from datetime import datetime, timedelta


def get_coordinates(address, failed_conversions):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = { "q": address, "format": "json" }
    try:
        response = requests.get(base_url, params, timeout = 10)
        response.raise_for_status()
        data = response.json()
        if data:
            latitude = float(data[0]["lat"])
            longitude = float(data[0]["lon"])
            return latitude, longitude
        else:
            failed_conversions["count"] += 1
            return "", ""
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        failed_conversions["count"] += 1
        return "", ""


def print_conversion_update(subject, start_time, conversion_count: int, total_address_count: int):

    indent = " " * (len(subject) + 2)

    elapsed_time = (datetime.now() - start_time).total_seconds() / 60
    conversion_percentage = conversion_count / total_address_count * 100
    conversion_rate = conversion_count / elapsed_time
    current_minute_message = f" Minute {elapsed_time:.0f} at {datetime.now().strftime('%H:%M:%S')} - "
    print(f"{indent}{current_minute_message}Converted {conversion_count:,} of {total_address_count:,} addresses at {conversion_rate:.1f} addresses per minute")
    
    projected_total_time = total_address_count / conversion_rate
    projected_remaining_time = projected_total_time - elapsed_time
    if projected_remaining_time >= 60:
        projected_remaining_time_message = f"{(projected_remaining_time / 60):.1f} hour(s)"
    else:
        projected_remaining_time_message = f"{projected_remaining_time:.1f} minutes"
    projected_total_end_time = (start_time + timedelta(minutes = projected_total_time)).strftime('%H:%M:%S')
    current_minute_indent = " " * (len(indent) + len(current_minute_message))
    print(f"{current_minute_indent}{conversion_percentage:.1f}% complete, projected to complete in {projected_remaining_time_message} at {projected_total_end_time}")
    return datetime.now()
    
    
def convert_addresses_to_coordinates(data: object, subject, candidate: str, purgatory_status: bool):
    data["full_address"] = data["contributor_street_1"] + ", " + data["contributor_city"] + ", " + data["contributor_state"] + " " + data["contributor_zip"]
    total_address_count = len(data["full_address"])
    if not purgatory_status:
        if total_address_count > 1000:
            print(f"\n{'-' * 100}\n{subject} | Added to purgatory list, will clean later. Address count: {total_address_count:,}")
            puragtory_candidate = candidate
            return None, puragtory_candidate
    start_time = datetime.now()
    print(f"\n{'-' * 100}\n{subject} | Starting to convert {total_address_count:,} addresses to coordinates at {start_time.strftime('%H:%M:%S')}")
    last_update_time = start_time
    conversion_count = 0
    failed_conversions = {"count": 0}
    for idx, address in enumerate(data["full_address"]):
        if "contribution_latitude" not in data.columns:
            data["contribution_latitude"] = None
        if "contribution_longitude" not in data.columns:
            data["contribution_longitude"] = None
        latitude, longitude = get_coordinates(address, failed_conversions)
        if latitude and longitude:
            data.at[idx, "contribution_latitude"] = latitude
            data.at[idx, "contribution_longitude"] = longitude
        else:
            data.at[idx, "contribution_latitude"] = None
            data.at[idx, "contribution_longitude"] = None
        conversion_count += 1
        minute_interval = 5
        if (datetime.now() - last_update_time).total_seconds() >= minute_interval * 60:
            last_update_time = print_conversion_update(subject, start_time, conversion_count, total_address_count)
    end_time = datetime.now()
    total_conversions = total_address_count - failed_conversions['count']
    total_time = (end_time - start_time).total_seconds() / 60
    conversion_rate = total_address_count / total_time
    print(f"{subject} | Finished converting {total_conversions:,} out of {total_address_count:,} addresses to coordinates in {total_time:.1f} minutes at {conversion_rate:.1f} addresses per minute")
    obsolete_columns = [
        "contributor_street_1", "contributor_city", "contributor_state", "contributor_zip", "full_address"
    ]
    data.drop(columns = obsolete_columns, inplace = True)
    return data, None