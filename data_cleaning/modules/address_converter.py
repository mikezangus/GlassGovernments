import requests
import time


def get_coordinates(address, failed_conversions):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = { "q": address, "format": "json" }
    try:
        response = requests.get(url = base_url, params = params, timeout = 10)
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
    
    
def convert_addresses_to_coordinates(data, subject):
    indent = ' ' * (len(subject) + 2)
    data["full_address"] = data["contributor_street_1"] + ", " + data["contributor_city"] + ", " + data["contributor_state"] + " " + data["contributor_zip"] 
    total_address_count = len(data["full_address"])
    conversion_start_time = time.time()
    print(f"\n{subject} | Starting to convert {format(total_address_count, ',')} addresses to coordinates at {time.strftime('%H:%M:%S', time.localtime(conversion_start_time))}")
    conversion_last_update_time = conversion_start_time
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
        if time.time() - conversion_last_update_time >= 300:
            loop_elapsed_time = (time.time() - conversion_start_time) / 60 
            loop_conversion_percentage = conversion_count / total_address_count * 100
            loop_conversion_rate = conversion_count / loop_elapsed_time
            projected_total_time = total_address_count / loop_conversion_rate
            projected_total_remaining_time = projected_total_time - loop_elapsed_time
            if projected_total_remaining_time >= 60:
                projected_total_remaining_time_printout = f"{(projected_total_remaining_time / 60):.1f} hour(s)"
            else:
                projected_total_remaining_time_printout = f"{(projected_total_remaining_time):.1f} minutes"
            projected_total_end_time = time.strftime('%H:%M:%S', time.localtime(conversion_start_time + projected_total_time * 60))
            loop_current_minute = f"Minute {int(loop_elapsed_time)} at {time.strftime('%H:%M:%S', time.localtime(time.time()))} | "
            print(f"{indent}{loop_current_minute} - Converted {format(conversion_count, ',')} of {format(total_address_count, ',')} addresses at {int(loop_conversion_rate)} addresses per minute")
            print(f"{indent + len(loop_current_minute)}{loop_conversion_percentage:.1f}% complete, projected to complete in {projected_total_remaining_time_printout} at {projected_total_end_time}")
            conversion_last_update_time = time.time()
    end_time = time.time()
    conversion_total_time = (end_time - conversion_start_time) / 60
    total_conversion_rate = total_address_count / conversion_total_time
    print(f"{subject} | Finished converting {format((total_address_count - failed_conversions['count']), ',')} out of {format(total_address_count, ',')} addresses to coordinates in {conversion_total_time:.2f} minutes at {total_conversion_rate:.2f} addresses per minute")
    data.drop(columns = ["contributor_street_1", "contributor_city", "contributor_state", "contributor_zip", "full_address"], inplace = True)
    return data