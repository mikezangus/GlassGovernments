import json
import os
import pandas as pd
import pymongo
import sys

coords_dir = os.path.dirname(__file__)
usa_dir = os.path.dirname(coords_dir)
geography_dir = os.path.dirname(usa_dir)
data_dir = os.path.dirname(geography_dir)
sys.path.append(data_dir)
from data.utils.directories import get_data_files_dir, get_config_file_path


def load_df_from_file() -> pd.DataFrame:
    path = os.path.join(get_data_files_dir(), "locations.csv")
    df = pd.read_csv(
        filepath_or_buffer = path,
        dtype = { "ZIP": str }
    )
    return df


def convert_to_geojson(df: pd.DataFrame) -> pd.DataFrame:
    df["COORDS"] = df.apply(
        lambda row:
            {
                "type": "Point",
                "coordinates":
                    [
                        row["LON"],
                        row["LAT"]
                    ]
            }
        if pd.notnull(row["LAT"]) and pd.notnull(row["LON"])
        else None, axis = 1
    )
    df.drop(
        columns = ["LAT", "LON"],
        inplace = True
    )
    return df


def get_mongo() -> str:
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = config["mongoUri"]
    db_name = config["mongoDatabase"]
    return uri, db_name


def upload_df(uri: str, db_name: str, df: pd.DataFrame) -> None:
    print("Started uploading")
    collection = "locations"
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    collection = db[collection]
    records = df.to_dict("records")
    collection.insert_many(records)
    client.close()
    print("Finished uploading")
    return


def main():
    df = load_df_from_file()
    df = convert_to_geojson(df)
    uri, db_name = get_mongo()
    upload_df(uri, db_name, df)


if __name__ == "__main__":
    main()
