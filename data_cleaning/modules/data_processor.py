import pandas as pd
import requests
import time


def process_raw_data(source_file_name, source_file_path):


    candidate_info = source_file_name.split("_")[:6]
    year, state, district, last_name, first_name, party = candidate_info
 

    def add_candidate_info(data, state, district, last_name, first_name, party):
        data["candidate_state"] = state
        data["candidate_district"] = district
        data["candidate_last_name"] = last_name
        data["candidate_first_name"] = first_name
        data["candidate_party"] = party
        return data
    
    
    def convert_addresses_to_coordinates(data):


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
                    return f"[{latitude}, {longitude}]"
                else:
                    failed_conversions["count"] += 1
                    return ""
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                failed_conversions["count"] += 1
                return ""
            

        data["full_address"] = data["contributor_street_1"] + ", " + data["contributor_city"] + ", " + data["contributor_state"] + " " + data["contributor_zip"] 
        total_address_count = len(data["full_address"])
        conversion_start_time = time.time()
        print(f"Starting to convert {format(total_address_count, ',')} addresses to coordinates at {time.strftime('%H:%M:%S', time.localtime(conversion_start_time))}")
        conversion_last_update_time = conversion_start_time
        conversion_count = 0
        failed_conversions = {"count": 0}
        for idx, address in enumerate(data["full_address"]):
            data.at[idx, "contribution_location"] = get_coordinates(address = address, failed_conversions = failed_conversions)
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
                print(f"{' ' * 9}{loop_current_minute}Converted {format(conversion_count, ',')} of {format(total_address_count, ',')} addresses at {int(loop_conversion_rate)} addresses per minute")
                print(f"{' ' * (9 + len(loop_current_minute))}{loop_conversion_percentage:.1f}% complete, projected to complete in {projected_total_remaining_time_printout} at {projected_total_end_time}")
                conversion_last_update_time = time.time()
        end_time = time.time()
        conversion_total_time = (end_time - conversion_start_time) / 60
        total_conversion_rate = total_address_count / conversion_total_time
        print(f"Finished converting {format((total_address_count - failed_conversions['count']), ',')} out of {format(total_address_count, ',')} addresses to coordinates in {conversion_total_time:.2f} minutes at {total_conversion_rate:.2f} addresses per minute")
        data.drop(columns = ["contributor_street_1", "contributor_city", "contributor_state", "contributor_zip", "full_address"], inplace = True)
        return data
    

    def clean_data():
        relevant_cols = [
            "transaction_id",
            "entity_type_desc",
            "contributor_street_1", "contributor_city", "contributor_state", "contributor_zip",
            "contribution_receipt_date", "contribution_receipt_amount",
            "candidate_name", "candidate_office_full", "candidate_office_state", "candidate_office_district",
            "donor_committee_name",
            "fec_election_type_desc", "fec_election_year"
        ]
        col_order = [
            "transaction_id",
            "candidate_last_name",
            "candidate_first_name",
            "fec_election_year",
            "candidate_state",
            "candidate_district",
            "candidate_party",
            "contribution_receipt_date",
            "contribution_receipt_amount",
            "entity_type_desc",
            "contribution_location",
            "fec_election_type_desc",
            "donor_committee_name",
            "candidate_office_full",
            "candidate_office_state",
            "candidate_office_district"
        ]
        data = pd.read_csv(
            filepath_or_buffer = source_file_path, sep = ",", usecols = relevant_cols, dtype = str, na_values = "", keep_default_na = False, low_memory = False
        )
        data = data[data["fec_election_year"] == year]
        data = add_candidate_info(data = data, state = state, district = district, last_name = last_name, first_name = first_name, party = party)
        data = convert_addresses_to_coordinates(data = data)
        data = data.reindex(columns = col_order)
        return data
    

    processed_data = clean_data()
    return processed_data
