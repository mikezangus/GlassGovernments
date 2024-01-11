import pandas as pd


def covert_data_types(input_file_path: str):
    data = pd.read_csv(
        filepath_or_buffer = input_file_path,
        sep = ",",
        dtype = {
            "election_year": str,
            "election_constituency": str,
            "contribution_amount": float,
            "contributor_office_district": str
        }
    )
    data["contribution_location"] = data.apply(
        lambda row: {
            "type": "Point",
            "coordinates": [
                row["contributor_longitude"],
                row["contributor_latitude"]
            ]
        }
        if pd.notnull(row["contributor_latitude"]) and pd.notnull(row["contributor_longitude"])
        else None, axis = 1
    )
    data.drop(
        columns = ["contributor_latitude", "contributor_longitude"],
        inplace = True
    )
    return data