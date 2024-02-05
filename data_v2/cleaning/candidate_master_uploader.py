import json
import os
import pandas as pd
import sys
from pathlib import Path
from pymongo import MongoClient, UpdateOne

cleaning_dir = Path(__file__).resolve().parent
data_dir = str(cleaning_dir.parent)
sys.path.append(data_dir)
from directories import get_config_file_path, get_cleaned_dir


def decide_year() -> str:
    year_dirs = os.listdir(get_cleaned_dir())
    year_options = [y for y in year_dirs if y.isdigit()]
    sorted_year_options = sorted(
        year_options,
        key = lambda x: int(x)
    )
    formatted_year_options = ', '.join(sorted_year_options)
    while True:
        year = input(f"\nFor which year do you want to clean raw data?\nAvailable years: {formatted_year_options}\n> ")
        if year in year_options:
            return year
        else:
            print(f"\n{year} isn't an available year, try again")


def connect_to_mongo():
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
    config["uri"] = uri
    client = MongoClient(config["uri"])
    db = client[config["mongoDatabase"]]
    print("Successfully connected to MongoDB")
    return db


def get_input_file_path(year: str) -> str:
    path = os.path.join(get_cleaned_dir(), year, "candidate_master.csv")
    return path


def load_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(
        filepath_or_buffer = path,
        sep = ",",
        dtype = str
    )
    return df


def upload_df(year: str, db, df: pd.DataFrame) -> None:
    collection_name = f"{year}_candidate_master"
    print(f"Starting to upload {len(df):,} records to collection {collection_name}")
    collection = db[collection_name]
    records = df.to_dict("records")
    operations = []
    for record in records:
        operations.append(UpdateOne(
            { "CAND_ID": record["CAND_ID"] },
            { "$setOnInsert": record },
            upsert = True
        ))
    if operations:
        result = collection.bulk_write(operations)
    print(f"Finished uploading {result.upserted_count:,} new records to collection {collection_name}")


def main():
    year = decide_year()
    db = connect_to_mongo()
    input_file_path = get_input_file_path(year)
    df = load_df(input_file_path)
    upload_df(year, db, df)



if __name__ == "__main__":
    main()