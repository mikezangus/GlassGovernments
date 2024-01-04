import pandas as pd


def covert_data_types(cleaned_file_path: str):
    data = pd.read_csv(filepath_or_buffer = cleaned_file_path, sep = ",")
    data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)
    data["contribution_location"] = data.apply(
        lambda row: {"type": "Point", "coordinates": [row["contribution_longitude"], row["contribution_latitude"]]}
        if pd.notnull(row["contribution_latitude"]) and pd.notnull(row["contribution_longitude"])
        else None, axis = 1
    )
    data.drop(columns=["contribution_latitude", "contribution_longitude"], inplace=True)
    return data