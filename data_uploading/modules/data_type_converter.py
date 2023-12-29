import pandas as pd


def covert_data_types(cleaned_file_path):
    data = pd.read_csv(filepath_or_buffer = cleaned_file_path, sep = ",")
    data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)
    data["contribution_location"] = data["contribution_location"].apply(
        lambda x: {"type": "Point", "coordinates": [float(coord) for coord in x.strip("[]").split(", ")[::-1]]} if isinstance(x, str) else None)
    return data